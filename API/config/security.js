const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const xss = require('xss-clean');
const hpp = require('hpp');
const cors = require('cors');
const mongoSanitize = require('express-mongo-sanitize');
const { randomBytes } = require('crypto');

// Auto-rotating CSRF token
const csrfProtection = (req, res, next) => {
    if (!req.session.csrfToken || Date.now() - req.session.csrfTimestamp > 3600000) {
        req.session.csrfToken = randomBytes(32).toString('hex');
        req.session.csrfTimestamp = Date.now();
    }
    res.locals.csrfToken = req.session.csrfToken;
    next();
};

// Auto-managed rate limiting
const createRateLimiter = (windowMs = 15 * 60 * 1000, max = 100) => rateLimit({
    windowMs,
    max,
    standardHeaders: true,
    legacyHeaders: false,
    skip: (req) => req.ip === '127.0.0.1',
    handler: (req, res) => {
        console.log(`Rate limit exceeded for IP: ${req.ip}`);
        res.status(429).json({
            success: false,
            message: 'Too many requests, please try again later.'
        });
    }
});

// Automatic security headers
const securityHeaders = helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'", 'https:'],
            scriptSrc: ["'self'", "'unsafe-inline'", 'https:'],
            imgSrc: ["'self'", 'data:', 'https:'],
            connectSrc: ["'self'", 'https://api.docmatrixai.com'],
            frameSrc: ["'none'"],
            objectSrc: ["'none'"]
        }
    },
    crossOriginEmbedderPolicy: true,
    crossOriginOpenerPolicy: true,
    crossOriginResourcePolicy: { policy: 'same-site' },
    dnsPrefetchControl: true,
    frameguard: { action: 'deny' },
    hidePoweredBy: true,
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    },
    ieNoOpen: true,
    noSniff: true,
    originAgentCluster: true,
    permittedCrossDomainPolicies: { permittedPolicies: 'none' },
    referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
    xssFilter: true
});

// Auto session management
const sessionConfig = {
    secret: process.env.SESSION_SECRET,
    name: 'sessionId',
    cookie: {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 24 * 60 * 60 * 1000 // 24 hours
    },
    resave: false,
    saveUninitialized: false,
    rolling: true
};

// Automated request sanitization
const sanitizeRequests = [
    mongoSanitize(), // Remove $ and . from requests
    xss(),           // Clean XSS
    hpp()            // Prevent HTTP Parameter Pollution
];

// CORS configuration
const corsOptions = {
    origin: process.env.CORS_ORIGIN,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
    maxAge: 600 // 10 minutes
};

// Auto-rotating API keys
class ApiKeyManager {
    static async rotateKey(userId) {
        const newKey = randomBytes(32).toString('hex');
        const expiresAt = new Date(Date.now() + 90 * 24 * 60 * 60 * 1000); // 90 days
        
        // Store in database
        await db.query(
            'INSERT INTO api_keys (userId, keyValue, expiresAt) VALUES (?, ?, ?)',
            [userId, newKey, expiresAt]
        );
        
        return { apiKey: newKey, expiresAt };
    }

    static async validateKey(apiKey) {
        const [key] = await db.query(
            'SELECT * FROM api_keys WHERE keyValue = ? AND expiresAt > NOW()',
            [apiKey]
        );
        return key ? true : false;
    }
}

module.exports = {
    csrfProtection,
    createRateLimiter,
    securityHeaders,
    sessionConfig,
    sanitizeRequests,
    corsOptions,
    ApiKeyManager
};
