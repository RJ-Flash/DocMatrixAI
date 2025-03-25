import request from 'supertest';
import app from '../app.js';
import { pool } from '../config/database.js';
import { logger } from '../utils/logger.js';
import jwt from 'jsonwebtoken';
import { commonValidations } from '../middleware/validate.js';
import bcrypt from 'bcryptjs';

describe('Auth Routes', () => {
    beforeAll(async () => {
        // Clear test data
        await pool.execute('DELETE FROM users WHERE email LIKE ?', ['%test%']);
        // Setup test database
        await pool.query(`
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);
    });

    afterAll(async () => {
        await pool.end();
        // Cleanup test database
        await pool.query('DROP TABLE IF EXISTS users');
    });

    describe('POST /api/auth/register', () => {
        it('should register a new user', async () => {
            const response = await request(app)
                .post('/api/auth/register')
                .send({
                    email: 'test@example.com',
                    password: 'Test123!',
                    name: 'Test User'
                });

            expect(response.status).toBe(201);
            expect(response.body).toHaveProperty('token');
            expect(response.body.user).toHaveProperty('id');
            expect(response.body.user.email).toBe('test@example.com');
            expect(response.body.user.name).toBe('Test User');
        });

        it('should validate required fields', async () => {
            const response = await request(app)
                .post('/api/auth/register')
                .send({});

            expect(response.status).toBe(400);
            expect(response.body).toHaveProperty('error', 'Validation Error');
        });
    });

    describe('POST /api/auth/login', () => {
        it('should return 400 for invalid credentials', async () => {
            const response = await request(app)
                .post('/api/auth/login')
                .send({
                    email: 'test@example.com',
                    password: 'wrongpassword'
                });

            expect(response.status).toBe(400);
            expect(response.body).toHaveProperty('status', 'error');
            expect(response.body).toHaveProperty('message', 'Invalid credentials');
        });

        it('should return 200 and token for valid credentials', async () => {
            // Insert test user
            await pool.query(
                'INSERT INTO users (email, password) VALUES (?, ?)',
                ['test@example.com', '$2b$10$testhash']
            );

            const response = await request(app)
                .post('/api/auth/login')
                .send({
                    email: 'test@example.com',
                    password: 'correctpassword'
                });

            expect(response.status).toBe(200);
            expect(response.body).toHaveProperty('status', 'success');
            expect(response.body).toHaveProperty('token');
            
            // Verify token
            const token = response.body.token;
            const decoded = jwt.verify(token, process.env.JWT_SECRET);
            expect(decoded).toHaveProperty('email', 'test@example.com');
        });
    });

    describe('POST /api/v1/auth/verify-email', () => {
        let verificationToken;

        beforeEach(async () => {
            const hashedPassword = await bcrypt.hash('Test123!@#', 10);
            verificationToken = 'test-token-123';
            
            await pool.execute(
                'INSERT INTO users (email, password, name, verification_token) VALUES (?, ?, ?, ?)',
                ['test@example.com', hashedPassword, 'Test User', verificationToken]
            );
        });

        it('should verify email with valid token', async () => {
            const res = await request(app)
                .post('/api/v1/auth/verify-email')
                .send({ token: verificationToken });

            expect(res.status).toBe(200);

            const [rows] = await pool.execute(
                'SELECT is_verified FROM users WHERE email = ?',
                ['test@example.com']
            );
            expect(rows[0].is_verified).toBe(1);
        });

        it('should not verify with invalid token', async () => {
            const res = await request(app)
                .post('/api/v1/auth/verify-email')
                .send({ token: 'invalid-token' });

            expect(res.status).toBe(400);
        });
    });
});
