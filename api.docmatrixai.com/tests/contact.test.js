import request from 'supertest';
import app from '../app.js';
import { pool } from '../config/database.js';
import { logger } from '../utils/logger.js';

describe('Contact Form Tests', () => {
    beforeAll(async () => {
        // Set up test database
        await pool.query(`
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);
    });

    afterAll(async () => {
        // Clean up test database
        await pool.query('DROP TABLE IF EXISTS contact_messages');
    });

    describe('POST /api/contact', () => {
        it('should return 400 for invalid input', async () => {
            const response = await request(app)
                .post('/api/contact')
                .send({
                    name: '',
                    email: 'invalid-email',
                    message: ''
                });

            expect(response.status).toBe(400);
            expect(response.body).toHaveProperty('status', 'error');
            expect(response.body).toHaveProperty('errors');
            expect(Array.isArray(response.body.errors)).toBe(true);
        });

        it('should save valid contact message', async () => {
            const messageData = {
                name: 'Test User',
                email: 'test@example.com',
                message: 'Test message'
            };

            const response = await request(app)
                .post('/api/contact')
                .send(messageData);

            expect(response.status).toBe(200);
            expect(response.body).toHaveProperty('status', 'success');
            expect(response.body).toHaveProperty('message', 'Message sent successfully');

            // Verify message was saved
            const [rows] = await pool.query(
                'SELECT * FROM contact_messages WHERE email = ?',
                [messageData.email]
            );

            expect(rows.length).toBe(1);
            expect(rows[0]).toMatchObject(messageData);
        });
    });
});
