const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const { promisify } = require('util');
const db = require('../config/database');
const EmailService = require('./email.service');
const { SecurityError } = require('../utils/errors');
const logger = require('../utils/logger');

class AuthService {
    static async register(userData) {
        const connection = await db.getConnection();
        try {
            await connection.beginTransaction();

            // Check if user exists
            const [existingUser] = await connection.query(
                'SELECT id FROM users WHERE email = ?',
                [userData.email]
            );

            if (existingUser.length > 0) {
                throw new SecurityError('Email already registered');
            }

            // Hash password
            const salt = await bcrypt.genSalt(12);
            const passwordHash = await bcrypt.hash(userData.password, salt);

            // Generate verification token
            const verificationToken = crypto.randomBytes(32).toString('hex');

            // Create user
            const userId = crypto.randomBytes(16);
            await connection.query(
                `INSERT INTO users (id, name, email, password_hash, company, verification_token)
                 VALUES (?, ?, ?, ?, ?, ?)`,
                [userId, userData.name, userData.email, passwordHash, userData.company, verificationToken]
            );

            // Send verification email
            await EmailService.sendVerificationEmail(userData.email, verificationToken);

            // Log the registration
            await connection.query(
                `INSERT INTO audit_logs (id, action, details, ip_address, user_agent)
                 VALUES (?, 'user_registered', ?, ?, ?)`,
                [
                    crypto.randomBytes(16),
                    JSON.stringify({ email: userData.email }),
                    userData.ip,
                    userData.userAgent
                ]
            );

            await connection.commit();
            return { success: true };
        } catch (error) {
            await connection.rollback();
            throw error;
        } finally {
            connection.release();
        }
    }

    static async login(email, password, ip, userAgent) {
        const connection = await db.getConnection();
        try {
            // Get user
            const [users] = await connection.query(
                'SELECT id, password_hash, status, email_verified FROM users WHERE email = ?',
                [email]
            );

            const user = users[0];

            // Log attempt
            await connection.query(
                `INSERT INTO login_attempts (id, email, ip_address, success)
                 VALUES (?, ?, ?, false)`,
                [crypto.randomBytes(16), email, ip]
            );

            // Check if user exists and verify password
            if (!user || !(await bcrypt.compare(password, user.password_hash))) {
                throw new SecurityError('Invalid credentials');
            }

            // Check account status
            if (user.status !== 'active') {
                throw new SecurityError('Account is not active');
            }

            if (!user.email_verified) {
                throw new SecurityError('Email not verified');
            }

            // Update login attempt to success
            await connection.query(
                'UPDATE login_attempts SET success = true WHERE email = ? ORDER BY created_at DESC LIMIT 1',
                [email]
            );

            // Update last login
            await connection.query(
                'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
                [user.id]
            );

            // Generate tokens
            const accessToken = jwt.sign(
                { userId: user.id },
                process.env.JWT_SECRET,
                { expiresIn: '15m' }
            );

            const refreshToken = jwt.sign(
                { userId: user.id },
                process.env.JWT_REFRESH_SECRET,
                { expiresIn: '7d' }
            );

            // Log successful login
            await connection.query(
                `INSERT INTO audit_logs (id, user_id, action, details, ip_address, user_agent)
                 VALUES (?, ?, 'user_login', ?, ?, ?)`,
                [
                    crypto.randomBytes(16),
                    user.id,
                    JSON.stringify({ ip, success: true }),
                    ip,
                    userAgent
                ]
            );

            return {
                accessToken,
                refreshToken
            };
        } finally {
            connection.release();
        }
    }

    static async verifyEmail(token) {
        const connection = await db.getConnection();
        try {
            await connection.beginTransaction();

            const [users] = await connection.query(
                'SELECT id FROM users WHERE verification_token = ?',
                [token]
            );

            if (users.length === 0) {
                throw new SecurityError('Invalid verification token');
            }

            await connection.query(
                `UPDATE users 
                 SET email_verified = true,
                     verification_token = NULL,
                     status = 'active'
                 WHERE id = ?`,
                [users[0].id]
            );

            // Log verification
            await connection.query(
                `INSERT INTO audit_logs (id, user_id, action)
                 VALUES (?, ?, 'email_verified')`,
                [crypto.randomBytes(16), users[0].id]
            );

            await connection.commit();
            return { success: true };
        } catch (error) {
            await connection.rollback();
            throw error;
        } finally {
            connection.release();
        }
    }

    static async requestPasswordReset(email) {
        const connection = await db.getConnection();
        try {
            const [users] = await connection.query(
                'SELECT id FROM users WHERE email = ?',
                [email]
            );

            if (users.length === 0) {
                // Return success even if email doesn't exist (security)
                return { success: true };
            }

            const resetToken = crypto.randomBytes(32).toString('hex');
            const expires = new Date();
            expires.setHours(expires.getHours() + 1);

            await connection.query(
                `UPDATE users 
                 SET reset_token = ?,
                     reset_token_expires = ?
                 WHERE id = ?`,
                [resetToken, expires, users[0].id]
            );

            await EmailService.sendPasswordResetEmail(email, resetToken);

            // Log reset request
            await connection.query(
                `INSERT INTO audit_logs (id, user_id, action)
                 VALUES (?, ?, 'password_reset_requested')`,
                [crypto.randomBytes(16), users[0].id]
            );

            return { success: true };
        } finally {
            connection.release();
        }
    }

    static async resetPassword(token, newPassword) {
        const connection = await db.getConnection();
        try {
            await connection.beginTransaction();

            const [users] = await connection.query(
                `SELECT id 
                 FROM users 
                 WHERE reset_token = ?
                 AND reset_token_expires > CURRENT_TIMESTAMP`,
                [token]
            );

            if (users.length === 0) {
                throw new SecurityError('Invalid or expired reset token');
            }

            const salt = await bcrypt.genSalt(12);
            const passwordHash = await bcrypt.hash(newPassword, salt);

            await connection.query(
                `UPDATE users 
                 SET password_hash = ?,
                     reset_token = NULL,
                     reset_token_expires = NULL
                 WHERE id = ?`,
                [passwordHash, users[0].id]
            );

            // Log password reset
            await connection.query(
                `INSERT INTO audit_logs (id, user_id, action)
                 VALUES (?, ?, 'password_reset_completed')`,
                [crypto.randomBytes(16), users[0].id]
            );

            await connection.commit();
            return { success: true };
        } catch (error) {
            await connection.rollback();
            throw error;
        } finally {
            connection.release();
        }
    }

    static async refreshToken(token) {
        try {
            const decoded = jwt.verify(token, process.env.JWT_REFRESH_SECRET);
            
            const accessToken = jwt.sign(
                { userId: decoded.userId },
                process.env.JWT_SECRET,
                { expiresIn: '15m' }
            );

            return { accessToken };
        } catch (error) {
            throw new SecurityError('Invalid refresh token');
        }
    }
}

module.exports = AuthService;
