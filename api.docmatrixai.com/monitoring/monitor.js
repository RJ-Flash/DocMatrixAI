import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { pool } from '../config/database.js';
import { logger } from '../utils/logger.js';

const execAsync = promisify(exec);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export async function checkSystemHealth() {
  try {
    const results = {
      status: 'success',
      checks: []
    };

    // Check disk space
    const { stdout: diskSpace } = await execAsync('df -h /');
    results.checks.push({
      type: 'disk',
      status: 'success',
      details: diskSpace
    });

    // Check memory usage
    const { stdout: memoryUsage } = await execAsync('free -m');
    results.checks.push({
      type: 'memory',
      status: 'success',
      details: memoryUsage
    });

    // Check CPU usage
    const { stdout: cpuUsage } = await execAsync('top -bn1');
    results.checks.push({
      type: 'cpu',
      status: 'success',
      details: cpuUsage
    });

    // Check database connection
    try {
      await pool.query('SELECT 1');
      results.checks.push({
        type: 'database',
        status: 'success',
        message: 'Database connection successful'
      });
    } catch (error) {
      results.checks.push({
        type: 'database',
        status: 'error',
        message: 'Database connection failed',
        error: error.message
      });
      results.status = 'error';
    }

    // Log health check results
    logger.info('System health check completed:', results);

    return results;
  } catch (error) {
    logger.error('Health check failed:', error);
    throw error;
  }
}

// Run health check if script is executed directly
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  checkSystemHealth()
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}
