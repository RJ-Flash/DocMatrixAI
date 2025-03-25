const db = require('./database');
const logger = require('../utils/logger');

class IPWhitelist {
    static async isWhitelisted(ip) {
        try {
            const [whitelist] = await db.query(
                'SELECT * FROM ip_whitelist WHERE ip_address = ? AND is_active = true',
                [ip]
            );
            return whitelist.length > 0;
        } catch (error) {
            logger.error('IP whitelist check failed:', error);
            return false;
        }
    }

    static async addToWhitelist(ip, description = '', expiresAt = null) {
        try {
            await db.query(
                `INSERT INTO ip_whitelist (ip_address, description, expires_at) 
                 VALUES (?, ?, ?)`,
                [ip, description, expiresAt]
            );
            logger.info(`IP ${ip} added to whitelist`);
            return true;
        } catch (error) {
            logger.error('Failed to add IP to whitelist:', error);
            return false;
        }
    }

    static async removeFromWhitelist(ip) {
        try {
            await db.query(
                'UPDATE ip_whitelist SET is_active = false WHERE ip_address = ?',
                [ip]
            );
            logger.info(`IP ${ip} removed from whitelist`);
            return true;
        } catch (error) {
            logger.error('Failed to remove IP from whitelist:', error);
            return false;
        }
    }

    static async getWhitelist() {
        try {
            const [whitelist] = await db.query(
                'SELECT * FROM ip_whitelist WHERE is_active = true'
            );
            return whitelist;
        } catch (error) {
            logger.error('Failed to get whitelist:', error);
            return [];
        }
    }
}

// Initialize IP whitelist table
const initWhitelistTable = async () => {
    try {
        await db.query(`
            CREATE TABLE IF NOT EXISTS ip_whitelist (
                id INT PRIMARY KEY AUTO_INCREMENT,
                ip_address VARCHAR(45) NOT NULL,
                description VARCHAR(255),
                is_active BOOLEAN DEFAULT true,
                expires_at DATETIME,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_ip (ip_address)
            )
        `);
        
        // Add localhost by default
        await IPWhitelist.addToWhitelist('127.0.0.1', 'Localhost');
        await IPWhitelist.addToWhitelist('::1', 'Localhost IPv6');
        
    } catch (error) {
        logger.error('Failed to initialize IP whitelist table:', error);
    }
};

initWhitelistTable();

module.exports = IPWhitelist;
