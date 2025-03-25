require('dotenv').config();
const bcrypt = require('bcryptjs');
const db = require('../config/database');
const { randomBytes } = require('crypto');

async function createAdmin() {
    try {
        // Generate secure password
        const tempPassword = randomBytes(16).toString('hex');
        const hashedPassword = await bcrypt.hash(tempPassword, 12);
        
        // Create admin user
        const [result] = await db.query(`
            INSERT INTO users (
                name,
                email,
                password,
                role,
                isVerified
            ) VALUES (?, ?, ?, 'admin', true)
        `, ['Admin User', 'admin@docmatrixai.com', hashedPassword]);

        console.log('\nAdmin account created successfully!');
        console.log('----------------------------------------');
        console.log('Email: admin@docmatrixai.com');
        console.log('Temporary Password:', tempPassword);
        console.log('----------------------------------------');
        console.log('Please change this password immediately after login!\n');

        process.exit(0);
    } catch (error) {
        console.error('Error creating admin:', error);
        process.exit(1);
    }
}

createAdmin();
