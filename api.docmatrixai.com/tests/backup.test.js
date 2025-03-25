import request from 'supertest';
import app from '../app.js';
import pool from '../config/database.js';
import { backup } from '../scripts/backup.js';
import fs from 'fs';
import path from 'path';

describe('Backup Routes', () => {
  const backupDir = path.join(process.cwd(), 'backups');

  beforeAll(async () => {
    // Create backup directory if it doesn't exist
    if (!fs.existsSync(backupDir)) {
      fs.mkdirSync(backupDir);
    }
  });

  afterAll(async () => {
    await pool.end();
    // Clean up test backup files
    const files = fs.readdirSync(backupDir);
    files.forEach(file => {
      if (file.startsWith('test-')) {
        fs.unlinkSync(path.join(backupDir, file));
      }
    });
  });

  describe('POST /api/backup/create', () => {
    it('should create a database backup', async () => {
      const response = await request(app)
        .post('/api/backup/create')
        .send({
          name: 'test-backup'
        });

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('message', 'Backup created successfully');
      expect(response.body).toHaveProperty('filename');
      
      const backupFile = path.join(backupDir, response.body.filename);
      expect(fs.existsSync(backupFile)).toBe(true);
    });

    it('should handle backup creation errors', async () => {
      // Mock the backup function to throw an error
      const originalBackup = backup;
      backup = async () => {
        throw new Error('Test error');
      };

      const response = await request(app)
        .post('/api/backup/create')
        .send({
          name: 'test-backup'
        });

      expect(response.status).toBe(500);
      expect(response.body).toHaveProperty('error', 'Failed to create backup');

      // Restore the original function
      backup = originalBackup;
    });
  });

  describe('GET /api/backup/list', () => {
    it('should list available backups', async () => {
      const response = await request(app)
        .get('/api/backup/list');

      expect(response.status).toBe(200);
      expect(Array.isArray(response.body)).toBe(true);
      expect(response.body.length).toBeGreaterThan(0);
      expect(response.body[0]).toHaveProperty('filename');
      expect(response.body[0]).toHaveProperty('createdAt');
      expect(response.body[0]).toHaveProperty('size');
    });

    it('should handle backup listing errors', async () => {
      // Mock fs.readdir to throw an error
      const originalReaddir = fs.readdir;
      fs.readdir = () => {
        throw new Error('Test error');
      };

      const response = await request(app)
        .get('/api/backup/list');

      expect(response.status).toBe(500);
      expect(response.body).toHaveProperty('error', 'Failed to list backups');

      // Restore the original function
      fs.readdir = originalReaddir;
    });
  });
}); 