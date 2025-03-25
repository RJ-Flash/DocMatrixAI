const logger = require('./logger');
const { ValidationError } = require('express-validator');
const mysql = require('mysql2');

class ErrorHandler {
    static async handle(err, req, res, next) {
        // Log error
        logger.error({
            message: err.message,
            stack: err.stack,
            path: req.path,
            method: req.method,
            ip: req.ip,
            timestamp: new Date().toISOString()
        });

        // Handle specific error types
        if (err instanceof ValidationError) {
            return res.status(400).json({
                success: false,
                error: 'Validation Error',
                details: err.errors
            });
        }

        if (err instanceof mysql.Error) {
            // Database errors
            switch (err.code) {
                case 'ER_DUP_ENTRY':
                    return res.status(409).json({
                        success: false,
                        error: 'Duplicate Entry'
                    });
                case 'ER_NO_REFERENCED_ROW':
                    return res.status(404).json({
                        success: false,
                        error: 'Referenced Resource Not Found'
                    });
                default:
                    // Don't expose internal DB errors
                    logger.error('Database Error:', err);
                    return res.status(500).json({
                        success: false,
                        error: 'Database Error'
                    });
            }
        }

        // Handle file upload errors
        if (err.code === 'LIMIT_FILE_SIZE') {
            return res.status(413).json({
                success: false,
                error: 'File Too Large'
            });
        }

        // Handle authentication errors
        if (err.name === 'JsonWebTokenError') {
            return res.status(401).json({
                success: false,
                error: 'Invalid Token'
            });
        }

        if (err.name === 'TokenExpiredError') {
            return res.status(401).json({
                success: false,
                error: 'Token Expired'
            });
        }

        // Rate limit errors
        if (err.status === 429) {
            return res.status(429).json({
                success: false,
                error: 'Too Many Requests',
                retryAfter: err.retryAfter
            });
        }

        // Security errors
        if (err.name === 'SecurityError') {
            return res.status(403).json({
                success: false,
                error: 'Security Violation'
            });
        }

        // Notify admin if critical
        if (err.critical) {
            // Send alert via email/SMS
            notifyAdmin(err);
        }

        // Default error
        res.status(500).json({
            success: false,
            error: 'Internal Server Error'
        });
    }

    static async notifyAdmin(err) {
        try {
            const nodemailer = require('nodemailer');
            const transporter = nodemailer.createTransport({
                host: process.env.SMTP_HOST,
                port: process.env.SMTP_PORT,
                secure: process.env.SMTP_PORT === '465',
                auth: {
                    user: process.env.SMTP_USER,
                    pass: process.env.SMTP_PASS
                }
            });

            await transporter.sendMail({
                from: process.env.FROM_EMAIL,
                to: 'admin@docmatrixai.com',
                subject: 'Critical Error Alert - DocMatrix AI',
                text: `
                    Critical Error Detected
                    
                    Error: ${err.message}
                    Stack: ${err.stack}
                    Time: ${new Date().toISOString()}
                    
                    Please check the logs for more details.
                `
            });
        } catch (error) {
            logger.error('Failed to send admin notification:', error);
        }
    }
}

module.exports = ErrorHandler;
