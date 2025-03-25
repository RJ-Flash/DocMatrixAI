import request from 'supertest';
import app from '../app.js';
import pool from '../config/database.js';

describe('Security Routes', () => {
  beforeAll(async () => {
    // Clear test data
    await pool.execute('DELETE FROM login_attempts WHERE ip_address LIKE ?', ['%test%']);
    await pool.execute('DELETE FROM blocked_ips WHERE ip_address LIKE ?', ['%test%']);
  });

  afterAll(async () => {
    await pool.end();
  });

  describe('POST /api/security/block-ip', () => {
    it('should block an IP address', async () => {
      const response = await request(app)
        .post('/api/security/block-ip')
        .send({
          ipAddress: '192.168.1.1',
          reason: 'Test blocking'
        });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('message', 'IP blocked successfully');
    });

    it('should validate IP address format', async () => {
      const response = await request(app)
        .post('/api/security/block-ip')
        .send({
          ipAddress: 'invalid-ip',
          reason: 'Test blocking'
        });

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error', 'Validation Error');
    });
  });

  describe('POST /api/security/unblock-ip', () => {
    it('should unblock an IP address', async () => {
      const response = await request(app)
        .post('/api/security/unblock-ip')
        .send({
          ipAddress: '192.168.1.1'
        });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('message', 'IP unblocked successfully');
    });

    it('should handle unblocking non-existent IP', async () => {
      const response = await request(app)
        .post('/api/security/unblock-ip')
        .send({
          ipAddress: '192.168.1.2'
        });

      expect(response.status).toBe(404);
      expect(response.body).toHaveProperty('error', 'IP not found');
    });
  });
}); 