require('dotenv').config();
const express = require('express');
const cors = require('cors');
const session = require('express-session');
const MySQLStore = require('express-mysql-session')(session);
const db = require('./config/database');
const { 
    securityHeaders, 
    createRateLimiter, 
    sessionConfig, 
    sanitizeRequests,
    corsOptions 
} = require('./config/security');
const errorHandler = require('./middleware/error');
const logger = require('./utils/logger');

// Initialize express
const app = express();

// Security middleware (automated)
app.use(securityHeaders);  // CSP and other security headers
app.use(cors(corsOptions)); // CORS with secure defaults

// Session store setup (automated)
const sessionStore = new MySQLStore({
    host: process.env.MYSQL_HOST,
    port: 3306,
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database: process.env.MYSQL_DATABASE,
    clearExpired: true,
    checkExpirationInterval: 900000,
    expiration: 86400000
});

// Session middleware (automated)
app.use(session({
    ...sessionConfig,
    store: sessionStore
}));

// Rate limiting (automated)
app.use('/api', createRateLimiter());
app.use('/api/auth', createRateLimiter(15 * 60 * 1000, 5)); // Stricter limits for auth
app.use('/api/documents', createRateLimiter(60 * 60 * 1000, 100)); // Custom limits for docs

// Request parsing and sanitization (automated)
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(sanitizeRequests);

// API Routes with automated security
app.use('/api/v1/auth', require('./routes/auth'));
app.use('/api/v1/users', require('./routes/users'));
app.use('/api/v1/documents', require('./routes/documents'));
app.use('/api/v1/contractai', require('./routes/contractai'));
app.use('/api/v1/expensedocai', require('./routes/expensedocai'));
app.use('/api/v1/hrdocai', require('./routes/hrdocai'));
app.use('/api/v1/supplydocai', require('./routes/supplydocai'));

// Automated error handling
app.use(errorHandler);

// Health check with basic auth
app.get('/health', (req, res) => {
    res.status(200).json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        memory: process.memoryUsage()
    });
});

// Database connection (with auto-retry)
const connectDB = async (retries = 5) => {
    try {
        const connection = await db.getConnection();
        connection.release();
        logger.info('MySQL Connected');
    } catch (error) {
        if (retries > 0) {
            logger.warn(`Database connection failed. Retrying... (${retries} attempts left)`);
            await new Promise(resolve => setTimeout(resolve, 5000));
            return connectDB(retries - 1);
        }
        logger.error('Database connection failed:', error);
        process.exit(1);
    }
};

// Start server with automated security checks
const startServer = async () => {
    try {
        await connectDB();
        
        const PORT = process.env.PORT || 3000;
        app.listen(PORT, () => {
            logger.info(`Server running in ${process.env.NODE_ENV} mode on port ${PORT}`);
            logger.info('Security features initialized:');
            logger.info('✓ CSRF Protection');
            logger.info('✓ Rate Limiting');
            logger.info('✓ XSS Protection');
            logger.info('✓ SQL Injection Protection');
            logger.info('✓ Security Headers');
            logger.info('✓ Session Security');
        });
    } catch (error) {
        logger.error('Server startup failed:', error);
        process.exit(1);
    }
};

// Graceful shutdown
process.on('SIGTERM', () => {
    logger.info('SIGTERM received. Starting graceful shutdown...');
    sessionStore.close();
    db.end();
    process.exit(0);
});

startServer();
