import express from 'express';
import { authenticateToken, requireRole } from '../middleware/auth.js';
import { validate, sanitizeInput } from '../middleware/validation.js';
import { logger } from '../utils/logger.js';

const router = express.Router();

// Health check route
router.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Protected route example
router.get('/protected', authenticateToken, (req, res) => {
  res.json({ message: 'This is a protected route', user: req.user });
});

// Admin route example
router.get('/admin', authenticateToken, requireRole(['admin']), (req, res) => {
  res.json({ message: 'This is an admin route', user: req.user });
});

// Validation example
router.post('/validate', sanitizeInput, validate, (req, res) => {
  res.json({ message: 'Validation passed', data: req.body });
});

export default router; 