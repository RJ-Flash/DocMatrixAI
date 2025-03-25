const mysql = require('mysql2/promise');
const logger = require('../utils/logger');

const pool = mysql.createPool({
    host: process.env.MYSQL_HOST || 'localhost',
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database: process.env.MYSQL_DATABASE,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// Test database connection
async function testConnection() {
    try {
        await pool.getConnection();
        logger.info('MySQL Database Connected');
    } catch (error) {
        logger.error('MySQL Connection Error:', error);
        process.exit(1);
    }
}

// Initialize database tables
async function initDatabase() {
    try {
        const connection = await pool.getConnection();

        // Users table
        await connection.query(`
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                isVerified BOOLEAN DEFAULT false,
                verificationToken VARCHAR(255),
                verificationExpire DATETIME,
                resetPasswordToken VARCHAR(255),
                resetPasswordExpire DATETIME,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        `);

        // Documents table
        await connection.query(`
            CREATE TABLE IF NOT EXISTS documents (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                originalName VARCHAR(255) NOT NULL,
                mimeType VARCHAR(100) NOT NULL,
                size INT NOT NULL,
                path VARCHAR(512) NOT NULL,
                status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
                processingType ENUM('contract', 'expense', 'hr', 'supply') NOT NULL,
                metadata JSON,
                userId INT NOT NULL,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (userId) REFERENCES users(id) ON DELETE CASCADE
            )
        `);

        connection.release();
        logger.info('Database tables initialized');
    } catch (error) {
        logger.error('Database initialization error:', error);
        process.exit(1);
    }
}

module.exports = {
    pool,
    testConnection,
    initDatabase
};
