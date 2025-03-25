import jwt from 'jsonwebtoken';
import rateLimit from 'express-rate-limit';
import helmet from 'helmet';
import cors from 'cors';
import { logger } from '../utils/logger.js';

// Define allowed origins based on environment
const allowedOrigins = process.env.NODE_ENV === 'production'
    ? ['https://docmatrixai.com', 'https://api.docmatrixai.com']
    : ['http://localhost:3000', 'http://localhost:3001'];

// Create rate limiter
const createRateLimiter = (windowMs = 15 * 60 * 1000, max = 100) => rateLimit({
    windowMs,
    max,
    message: 'Too many requests from this IP, please try again later.'
});

// Configure CORS options
const corsOptions = {
    origin: (origin, callback) => {
        if (!origin || allowedOrigins.includes(origin)) {
            callback(null, true);
        } else {
            callback(new Error('Not allowed by CORS'));
        }
    },
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true
};

// JWT verification middleware
const verifyToken = (req, res, next) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        
        if (!token) {
            return res.status(401).json({
                status: 'error',
                message: 'No token provided'
            });
        }

        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded;
        next();
    } catch (error) {
        logger.error('Token verification failed:', error);
        return res.status(401).json({
            status: 'error',
            message: 'Invalid token'
        });
    }
};

// Security headers
const securityHeaders = helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", 'data:', 'https:'],
            connectSrc: ["'self'", ...allowedOrigins],
            fontSrc: ["'self'", 'https:', 'data:'],
            objectSrc: ["'none'"],
            mediaSrc: ["'self'"],
            frameSrc: ["'none'"]
        }
    }
});

// Global rate limiter
const globalLimiter = createRateLimiter();

// Export security middleware array
const securityMiddleware = [
    // Log all requests
    (req, res, next) => {
        logger.info(`${req.method} ${req.path} - ${req.ip}`);
        next();
    },
    // Apply security headers
    securityHeaders,
    // Apply CORS
    cors(corsOptions),
    // Apply rate limiting
    globalLimiter
];

export {
    securityMiddleware,
    verifyToken,
    createRateLimiter
};
