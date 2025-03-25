import request from 'supertest';
import app from '../app.js';
import pool from '../config/database.js';
import { migrate } from '../scripts/migrate.js';
import fs from 'fs';
import path from 'path';

describe('Migration Routes', () => {
  const migrationsDir = path.join(process.cwd(), 'migrations');

  beforeAll(async () => {
    // Create migrations directory if it doesn't exist
    if (!fs.existsSync(migrationsDir)) {
      fs.mkdirSync(migrationsDir);
    }
  });

  afterAll(async () => {
    await pool.end();
    // Clean up test migration files
    const files = fs.readdirSync(migrationsDir);
    files.forEach(file => {
      if (file.startsWith('test-')) {
        fs.unlinkSync(path.join(migrationsDir, file));
      }
    });
  });

  describe('POST /api/migrate/run', () => {
    it('should run pending migrations', async () => {
      // Create a test migration file
      const testMigration = path.join(migrationsDir, 'test-001.sql');
      fs.writeFileSync(testMigration, 'CREATE TABLE test_table (id INT PRIMARY KEY);');

      const response = await request(app)
        .post('/api/migrate/run');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('message', 'Migrations completed successfully');
      expect(response.body).toHaveProperty('executedMigrations');
      expect(Array.isArray(response.body.executedMigrations)).toBe(true);
      expect(response.body.executedMigrations.length).toBeGreaterThan(0);

      // Clean up test table
      await pool.execute('DROP TABLE IF EXISTS test_table');
    });

    it('should handle migration errors', async () => {
      // Create an invalid test migration file
      const testMigration = path.join(migrationsDir, 'test-002.sql');
      fs.writeFileSync(testMigration, 'INVALID SQL STATEMENT;');

      const response = await request(app)
        .post('/api/migrate/run');

      expect(response.status).toBe(500);
      expect(response.body).toHaveProperty('error', 'Failed to run migrations');
    });
  });

  describe('GET /api/migrate/status', () => {
    it('should return migration status', async () => {
      const response = await request(app)
        .get('/api/migrate/status');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('pendingMigrations');
      expect(response.body).toHaveProperty('executedMigrations');
      expect(Array.isArray(response.body.pendingMigrations)).toBe(true);
      expect(Array.isArray(response.body.executedMigrations)).toBe(true);
    });

    it('should handle status retrieval errors', async () => {
      // Mock fs.readdir to throw an error
      const originalReaddir = fs.readdir;
      fs.readdir = () => {
        throw new Error('Test error');
      };

      const response = await request(app)
        .get('/api/migrate/status');

      expect(response.status).toBe(500);
      expect(response.body).toHaveProperty('error', 'Failed to get migration status');

      // Restore the original function
      fs.readdir = originalReaddir;
    });
  });
}); 