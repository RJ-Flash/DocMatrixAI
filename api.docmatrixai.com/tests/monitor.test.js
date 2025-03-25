import request from 'supertest';
import app from '../app.js';
import pool from '../config/database.js';
import { SystemMonitor } from '../monitoring/monitor.js';

describe('Monitoring Routes', () => {
  let monitor;

  beforeAll(async () => {
    monitor = new SystemMonitor();
  });

  afterAll(async () => {
    await pool.end();
  });

  describe('GET /api/monitor/metrics', () => {
    it('should return system metrics', async () => {
      const response = await request(app)
        .get('/api/monitor/metrics');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('cpu');
      expect(response.body).toHaveProperty('memory');
      expect(response.body).toHaveProperty('disk');
      expect(response.body).toHaveProperty('uptime');
      expect(response.body).toHaveProperty('timestamp');
    });

    it('should handle metric collection errors', async () => {
      // Mock the collectMetrics method to throw an error
      const originalCollectMetrics = monitor.collectMetrics;
      monitor.collectMetrics = async () => {
        throw new Error('Test error');
      };

      const response = await request(app)
        .get('/api/monitor/metrics');

      expect(response.status).toBe(500);
      expect(response.body).toHaveProperty('error', 'Failed to collect metrics');

      // Restore the original method
      monitor.collectMetrics = originalCollectMetrics;
    });
  });

  describe('GET /api/monitor/alerts', () => {
    it('should return system alerts', async () => {
      const response = await request(app)
        .get('/api/monitor/alerts');

      expect(response.status).toBe(200);
      expect(Array.isArray(response.body)).toBe(true);
    });

    it('should handle alert retrieval errors', async () => {
      // Mock the checkThresholds method to throw an error
      const originalCheckThresholds = monitor.checkThresholds;
      monitor.checkThresholds = async () => {
        throw new Error('Test error');
      };

      const response = await request(app)
        .get('/api/monitor/alerts');

      expect(response.status).toBe(500);
      expect(response.body).toHaveProperty('error', 'Failed to retrieve alerts');

      // Restore the original method
      monitor.checkThresholds = originalCheckThresholds;
    });
  });
}); 