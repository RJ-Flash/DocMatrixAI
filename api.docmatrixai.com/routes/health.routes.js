import express from 'express';
import { pool } from '../config/database.js';
import { checkSystemHealth } from '../monitoring/monitor.js';
import { logger } from '../utils/logger.js';

const router = express.Router();

// Basic health check
router.get('/', async (req, res) => {
    try {
        // Check database connection
        const connection = await pool.getConnection();
        connection.release();

        res.json({
            status: 'healthy',
            timestamp: new Date().toISOString(),
            uptime: process.uptime(),
            environment: process.env.NODE_ENV
        });
    } catch (err) {
        logger.error('Health check failed:', err);
        res.status(503).json({
            status: 'unhealthy',
            timestamp: new Date().toISOString(),
            error: err.message
        });
    }
});

// Detailed health check
router.get('/detailed', async (req, res) => {
    try {
        const healthData = await checkSystemHealth();
        res.json({
            status: 'healthy',
            ...healthData
        });
    } catch (err) {
        logger.error('Detailed health check failed:', err);
        res.status(503).json({
            status: 'unhealthy',
            timestamp: new Date().toISOString(),
            error: err.message
        });
    }
});

export default router;
