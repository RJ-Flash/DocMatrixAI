import dotenv from 'dotenv';
import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { logger } from '../utils/logger.js';

// Load environment variables
dotenv.config();

const execAsync = promisify(exec);
const writeFileAsync = promisify(fs.writeFile);
const mkdirAsync = promisify(fs.mkdir);

// Backup configuration
const config = {
    backupDir: process.env.BACKUP_DIR || './backups',
    dbHost: process.env.DB_HOST,
    dbUser: process.env.DB_USER,
    dbPassword: process.env.DB_PASSWORD,
    dbName: process.env.DB_NAME
};

// Create backup directory if it doesn't exist
const initBackupDir = async () => {
    try {
        await mkdirAsync(config.backupDir, { recursive: true });
        logger.info(`Backup directory created: ${config.backupDir}`);
    } catch (error) {
        if (error.code !== 'EEXIST') {
            logger.error('Failed to create backup directory:', error);
            throw error;
        }
    }
};

// Generate backup filename
const getBackupFilename = () => {
    const date = new Date().toISOString().replace(/[:.]/g, '-');
    return path.join(config.backupDir, `backup-${date}.sql`);
};

// Perform database backup
const backupDatabase = async () => {
    const backupFile = getBackupFilename();
    const command = `mysqldump -h ${config.dbHost} -u ${config.dbUser} -p${config.dbPassword} ${config.dbName} > ${backupFile}`;

    try {
        await initBackupDir();
        await execAsync(command);
        logger.info(`Database backup created: ${backupFile}`);

        // Create backup log
        const logEntry = {
            timestamp: new Date().toISOString(),
            file: backupFile,
            size: fs.statSync(backupFile).size
        };

        await writeFileAsync(
            path.join(config.backupDir, 'backup-log.json'),
            JSON.stringify(logEntry, null, 2)
        );

        return { success: true, file: backupFile };
    } catch (error) {
        logger.error('Database backup failed:', error);
        throw error;
    }
};

// Clean up old backups
const cleanupOldBackups = async (retentionDays = 7) => {
    try {
        const files = await fs.promises.readdir(config.backupDir);
        const now = new Date();

        for (const file of files) {
            if (!file.endsWith('.sql')) continue;

            const filePath = path.join(config.backupDir, file);
            const stats = await fs.promises.stat(filePath);
            const daysOld = (now - stats.mtime) / (1000 * 60 * 60 * 24);

            if (daysOld > retentionDays) {
                await fs.promises.unlink(filePath);
                logger.info(`Deleted old backup: ${file}`);
            }
        }
    } catch (error) {
        logger.error('Backup cleanup failed:', error);
        throw error;
    }
};

// Main backup process
const runBackup = async () => {
    try {
        await backupDatabase();
        await cleanupOldBackups();
        logger.info('Backup process completed successfully');
    } catch (error) {
        logger.error('Backup process failed:', error);
        process.exit(1);
    }
};

// Run backup if called directly
if (process.argv[1] === fileURLToPath(import.meta.url)) {
    runBackup();
}

export { runBackup, backupDatabase, cleanupOldBackups };
