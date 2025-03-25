import request from 'supertest';
import app from '../app.js';
import { logger } from '../utils/logger.js';

describe('Health Check Tests', () => {
    describe('GET /health', () => {
        it('should return basic health status', async () => {
            const response = await request(app).get('/health');

            expect(response.status).toBe(200);
            expect(response.body).toHaveProperty('status', 'healthy');
            expect(response.body).toHaveProperty('timestamp');
            expect(response.body).toHaveProperty('uptime');
            expect(response.body).toHaveProperty('environment');
        });
    });

    describe('GET /api/health/detailed', () => {
        it('should return detailed health status', async () => {
            const response = await request(app).get('/api/health/detailed');

            expect(response.status).toBe(200);
            expect(response.body).toHaveProperty('status', 'healthy');
            expect(response.body).toHaveProperty('timestamp');
            expect(response.body).toHaveProperty('diskSpace');
            expect(response.body).toHaveProperty('memoryUsage');
            expect(response.body).toHaveProperty('cpuUsage');
            expect(response.body).toHaveProperty('dbStatus');
        });
    });
});
