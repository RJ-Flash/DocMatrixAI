const crypto = require('crypto');
const { promisify } = require('util');
const jwt = require('jsonwebtoken');
const db = require('../config/database');

// Automated password security
class PasswordSecurity {
    static async validateComplexity(password) {
        const minLength = 12;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        
        return password.length >= minLength && 
               hasUpperCase && hasLowerCase && 
               hasNumbers && hasSpecialChar;
    }

    static async hashPassword(password) {
        const salt = await promisify(crypto.randomBytes)(32);
        const hash = await promisify(crypto.pbkdf2)(
            password,
            salt,
            10000,
            64,
            'sha512'
        );
        return `${salt.toString('hex')}:${hash.toString('hex')}`;
    }
}

// Automated login security
class LoginSecurity {
    static async trackLoginAttempt(email, success) {
        await db.query(
            `INSERT INTO login_attempts (email, success, ip_address) 
             VALUES (?, ?, ?)`,
            [email, success, req.ip]
        );

        if (!success) {
            const attempts = await db.query(
                `SELECT COUNT(*) as count FROM login_attempts 
                 WHERE email = ? AND success = false 
                 AND created_at > DATE_SUB(NOW(), INTERVAL 15 MINUTE)`,
                [email]
            );

            if (attempts[0].count >= 5) {
                await db.query(
                    `UPDATE users SET account_locked = true, 
                     locked_until = DATE_ADD(NOW(), INTERVAL 1 HOUR) 
                     WHERE email = ?`,
                    [email]
                );
                throw new Error('Account locked due to too many failed attempts');
            }
        }
    }
}

// Automated session security
class SessionSecurity {
    static async validateSession(req) {
        const token = req.cookies.token || req.headers.authorization?.split(' ')[1];
        
        if (!token) {
            throw new Error('No token provided');
        }

        try {
            const decoded = await promisify(jwt.verify)(token, process.env.JWT_SECRET);
            
            // Check if token is in blacklist
            const blacklisted = await db.query(
                'SELECT * FROM token_blacklist WHERE token = ?',
                [token]
            );
            
            if (blacklisted.length > 0) {
                throw new Error('Token has been invalidated');
            }

            // Check if user's password hasn't changed
            const user = await db.query(
                'SELECT password_changed_at FROM users WHERE id = ?',
                [decoded.id]
            );

            if (user[0].password_changed_at && 
                decoded.iat * 1000 < new Date(user[0].password_changed_at).getTime()) {
                throw new Error('User recently changed password');
            }

            return decoded;
        } catch (error) {
            throw new Error('Invalid token');
        }
    }

    static async rotateToken(user) {
        const token = jwt.sign(
            { id: user.id },
            process.env.JWT_SECRET,
            { expiresIn: process.env.JWT_EXPIRE }
        );

        return token;
    }
}

// File upload security
class FileUploadSecurity {
    static validateFileType(file) {
        const allowedTypes = process.env.ALLOWED_FILE_TYPES.split(',');
        const fileExt = file.originalname.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExt)) {
            throw new Error('Invalid file type');
        }

        // Check file signature (magic numbers)
        const signatures = {
            pdf: ['25504446'],
            doc: ['D0CF11E0'],
            docx: ['504B0304'],
            xls: ['D0CF11E0'],
            xlsx: ['504B0304']
        };

        const buffer = file.buffer.toString('hex', 0, 4).toUpperCase();
        const validSignature = signatures[fileExt].some(sig => buffer.startsWith(sig));
        
        if (!validSignature) {
            throw new Error('Invalid file signature');
        }
    }

    static async scanFile(file) {
        // Implement virus scanning here
        // This is a placeholder for actual implementation
        return new Promise(resolve => {
            setTimeout(() => {
                resolve({
                    safe: true,
                    threats: []
                });
            }, 1000);
        });
    }
}

module.exports = {
    PasswordSecurity,
    LoginSecurity,
    SessionSecurity,
    FileUploadSecurity
};
