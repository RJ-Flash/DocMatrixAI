import { logger } from '../utils/logger.js';
import { ValidationError } from 'express-validator';

const errorHandler = (err, req, res, _next) => {
    // Log the error
    logger.error('Error:', err);

    // Handle validation errors
    if (err instanceof ValidationError) {
        return res.status(400).json({
            status: 'error',
            message: 'Validation failed',
            errors: err.array()
        });
    }

    // Handle database errors
    if (err.code === 'ER_DUP_ENTRY') {
        return res.status(409).json({
            status: 'error',
            message: 'Duplicate entry found'
        });
    }

    // Handle JWT errors
    if (err.name === 'JsonWebTokenError') {
        return res.status(401).json({
            status: 'error',
            message: 'Invalid token'
        });
    }

    if (err.name === 'TokenExpiredError') {
        return res.status(401).json({
            status: 'error',
            message: 'Token expired'
        });
    }

    // Default error response
    return res.status(500).json({
        status: 'error',
        message: 'Internal server error'
    });
};

export default errorHandler;
