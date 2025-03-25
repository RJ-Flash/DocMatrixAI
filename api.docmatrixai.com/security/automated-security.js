import { exec } from 'child_process';
import { promisify } from 'util';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { pool } from '../config/database.js';
import { logger } from '../utils/logger.js';
import nodemailer from 'nodemailer';

const execAsync = promisify(exec);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Security monitoring and automated response system
const securityMonitor = {
  // Track security events
  isAccountLocked: false,
  fileChanges: [],
  vulnerableDependencies: [],

  // Monitor login attempts
  async monitorLoginAttempts() {
    try {
      const [rows] = await pool.query(
        'SELECT COUNT(*) as attempts FROM login_attempts WHERE timestamp > DATE_SUB(NOW(), INTERVAL 15 MINUTE)'
      );
      
      if (rows.attempts > 5) {
        this.isAccountLocked = true;
        await this.notifySecurityTeam('Multiple failed login attempts detected');
      }
    } catch (error) {
      logger.error('Error monitoring login attempts:', error);
    }
  },

  // Monitor file system changes
  async monitorFileChanges() {
    try {
      const [rows] = await pool.query(
        'SELECT * FROM file_changes WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)'
      );
      
      if (rows.length > 0) {
        this.fileChanges = rows;
        await this.notifySecurityTeam('Suspicious file system changes detected');
      }
    } catch (error) {
      logger.error('Error monitoring file changes:', error);
    }
  },

  // Check for vulnerable dependencies
  async checkDependencies() {
    try {
      const [rows] = await pool.query(
        'SELECT * FROM dependency_vulnerabilities WHERE severity = "high"'
      );
      
      if (rows.length > 0) {
        this.vulnerableDependencies = rows;
        await this.notifySecurityTeam('High severity vulnerabilities detected');
      }
    } catch (error) {
      logger.error('Error checking dependencies:', error);
    }
  },

  // Send security notifications
  async notifySecurityTeam(message) {
    try {
      const transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port: process.env.SMTP_PORT,
        secure: true,
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASS
        }
      });

      await transporter.sendMail({
        from: process.env.SMTP_FROM,
        to: process.env.SECURITY_TEAM_EMAIL,
        subject: 'Security Alert',
        text: message,
        html: `<p>${message}</p>`
      });
    } catch (error) {
      logger.error('Error sending security notification:', error);
    }
  },

  // Check for suspicious login attempts
  async checkLoginAttempts(userId) {
    try {
      const [rows] = await pool.query(
        'SELECT COUNT(*) as attempts FROM login_attempts WHERE user_id = ? AND timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)',
        [userId]
      );
      return rows[0].attempts;
    } catch (error) {
      logger.error('Error checking login attempts:', error);
      throw error;
    }
  },

  // Monitor for unusual database access patterns
  async monitorDatabaseAccess() {
    try {
      const [rows] = await pool.query(
        'SELECT user_id, COUNT(*) as access_count FROM access_logs WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR) GROUP BY user_id'
      );
      return rows;
    } catch (error) {
      logger.error('Error monitoring database access:', error);
      throw error;
    }
  },

  // Check for file system changes
  async checkFileSystemChanges() {
    try {
      const [rows] = await pool.query(
        'SELECT * FROM file_changes WHERE timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)'
      );
      return rows;
    } catch (error) {
      logger.error('Error checking file system changes:', error);
      throw error;
    }
  },

  // Monitor system resources
  async monitorSystemResources() {
    try {
      const [rows] = await pool.query(
        'SELECT * FROM system_metrics WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)'
      );
      return rows;
    } catch (error) {
      logger.error('Error monitoring system resources:', error);
      throw error;
    }
  },

  // Get security metrics
  async getSecurityMetrics() {
    try {
      const [rows] = await pool.query(
        'SELECT * FROM security_metrics WHERE timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)'
      );
      return rows;
    } catch (error) {
      logger.error('Error getting security metrics:', error);
      throw error;
    }
  },

  // Send security alerts
  async sendSecurityAlert(alertType, details) {
    const transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: process.env.SMTP_PORT,
      secure: true,
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
      }
    });

    const mailOptions = {
      from: process.env.ALERT_FROM_EMAIL,
      to: process.env.ALERT_TO_EMAIL,
      subject: `Security Alert: ${alertType}`,
      text: `
        Security Alert Details:
        Type: ${alertType}
        Time: ${new Date().toISOString()}
        Details: ${JSON.stringify(details, null, 2)}
      `
    };

    try {
      await transporter.sendMail(mailOptions);
      logger.info(`Security alert sent: ${alertType}`);
    } catch (error) {
      logger.error('Error sending security alert:', error);
      throw error;
    }
  },

  // Generate security report
  async generateSecurityReport() {
    const report = {
      timestamp: new Date().toISOString(),
      isAccountLocked: await this.checkLoginAttempts(null),
      fileChanges: await this.checkFileSystemChanges(),
      vulnerableDependencies: await this.checkDependencies(),
      systemMetrics: await this.monitorSystemResources(),
      securityMetrics: await this.getSecurityMetrics()
    };

    return report;
  }
};

export class AutomatedSecurity {
  constructor() {
    this.transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: process.env.SMTP_PORT,
      secure: true,
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
      }
    });
  }

  async checkFailedLoginAttempts() {
    try {
      const [rows] = await pool.execute(
        'SELECT ip_address, COUNT(*) as attempts FROM login_attempts WHERE success = false AND timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR) GROUP BY ip_address HAVING attempts >= 5'
      );

      for (const row of rows) {
        await this.blockIP(row.ip_address, 'Multiple failed login attempts');
        await this.notifyAdmin('Multiple failed login attempts detected', {
          ip: row.ip_address,
          attempts: row.attempts
        });
      }
    } catch (error) {
      logger.error('Failed to check login attempts:', error);
    }
  }

  async checkAccountTakeoverAttempts() {
    try {
      const [rows] = await pool.execute(
        'SELECT user_id, COUNT(*) as attempts FROM login_attempts WHERE success = false AND timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR) GROUP BY user_id HAVING attempts >= 3'
      );

      for (const row of rows) {
        await this.lockAccount(row.user_id);
        await this.notifyAdmin('Account takeover attempt detected', {
          userId: row.user_id,
          attempts: row.attempts
        });
      }
    } catch (error) {
      logger.error('Failed to check account takeover attempts:', error);
    }
  }

  async cleanupOldLoginAttempts() {
    try {
      await pool.execute(
        'DELETE FROM login_attempts WHERE timestamp < DATE_SUB(NOW(), INTERVAL 24 HOUR)'
      );
    } catch (error) {
      logger.error('Failed to cleanup login attempts:', error);
    }
  }

  async blockIP(ipAddress, reason) {
    try {
      await pool.execute(
        'INSERT INTO blocked_ips (ip_address, reason, blocked_at) VALUES (?, ?, NOW())',
        [ipAddress, reason]
      );
      logger.info(`Blocked IP address: ${ipAddress}`);
    } catch (error) {
      logger.error('Failed to block IP:', error);
    }
  }

  async lockAccount(userId) {
    try {
      await pool.execute(
        'UPDATE users SET is_locked = true, locked_at = NOW() WHERE id = ?',
        [userId]
      );
      logger.info(`Locked account: ${userId}`);
    } catch (error) {
      logger.error('Failed to lock account:', error);
    }
  }

  async notifyAdmin(subject, data) {
    try {
      await this.transporter.sendMail({
        from: process.env.SMTP_FROM,
        to: process.env.ADMIN_EMAIL,
        subject: `Security Alert: ${subject}`,
        text: JSON.stringify(data, null, 2)
      });
      logger.info(`Sent security notification: ${subject}`);
    } catch (error) {
      logger.error('Failed to send security notification:', error);
    }
  }

  async checkSystemSecurity() {
    try {
      // Check for file changes
      const { stdout: fileChanges } = await execAsync('git status --porcelain');
      if (fileChanges) {
        await this.notifyAdmin('File changes detected', { changes: fileChanges });
      }

      // Check for vulnerable dependencies
      const { stdout: vulnerabilities } = await execAsync('npm audit');
      if (vulnerabilities.includes('found')) {
        await this.notifyAdmin('Vulnerable dependencies detected', { audit: vulnerabilities });
      }

      // Check for account lockouts
      const [lockedAccounts] = await pool.execute(
        'SELECT id, email, locked_at FROM users WHERE is_locked = true'
      );
      if (lockedAccounts.length > 0) {
        await this.notifyAdmin('Locked accounts detected', { accounts: lockedAccounts });
      }
    } catch (error) {
      logger.error('Failed to check system security:', error);
    }
  }

  async monitorFileChanges() {
    try {
      const files = await fs.promises.readdir(path.join(process.cwd(), 'public'));
      for (const file of files) {
        const filePath = path.join(process.cwd(), 'public', file);
        const stats = await fs.promises.stat(filePath);
        const hash = await this.calculateFileHash(filePath);

        // Check if file has changed
        const [existingHash] = await pool.execute(
          'SELECT hash FROM file_hashes WHERE file_path = ?',
          [filePath]
        );

        if (existingHash.length === 0) {
          await pool.execute(
            'INSERT INTO file_hashes (file_path, hash, last_modified) VALUES (?, ?, ?)',
            [filePath, hash, stats.mtime]
          );
        } else if (existingHash[0].hash !== hash) {
          await this.sendSecurityAlert('File Change Detected', `File ${file} has been modified`);
          await pool.execute(
            'UPDATE file_hashes SET hash = ?, last_modified = ? WHERE file_path = ?',
            [hash, stats.mtime, filePath]
          );
        }
      }
    } catch (error) {
      logger.error('Error monitoring file changes:', error);
    }
  }

  async monitorDependencies() {
    try {
      const { stdout } = await execAsync('npm audit');
      const vulnerabilities = stdout.match(/found (\d+) vulnerabilities/);
      if (vulnerabilities && parseInt(vulnerabilities[1]) > 0) {
        await this.sendSecurityAlert('Dependency Vulnerabilities', `Found ${vulnerabilities[1]} vulnerabilities in dependencies`);
      }
    } catch (error) {
      logger.error('Error monitoring dependencies:', error);
    }
  }

  async sendSecurityAlert(subject, message) {
    try {
      await this.transporter.sendMail({
        from: process.env.SMTP_FROM,
        to: process.env.SECURITY_ALERT_EMAIL,
        subject: `Security Alert: ${subject}`,
        text: message
      });
    } catch (error) {
      logger.error('Error sending security alert:', error);
    }
  }

  async calculateFileHash(filePath) {
    const fileBuffer = await fs.promises.readFile(filePath);
    const crypto = await import('crypto');
    return crypto.createHash('sha256').update(fileBuffer).digest('hex');
  }
}

// Initialize and start monitoring
const security = new AutomatedSecurity();

// Monitor suspicious activity every 5 minutes
setInterval(() => security.checkFailedLoginAttempts(), 5 * 60 * 1000);

// Monitor file changes every hour
setInterval(() => security.monitorFileChanges(), 60 * 60 * 1000);

// Monitor dependencies daily
setInterval(() => security.monitorDependencies(), 24 * 60 * 60 * 1000);

export async function checkSecurity() {
  try {
    const results = {
      status: 'success',
      checks: []
    };

    // Check for outdated dependencies
    const { stdout: outdatedDeps } = await execAsync('npm outdated');
    if (outdatedDeps) {
      results.checks.push({
        type: 'dependencies',
        status: 'warning',
        message: 'Outdated dependencies found',
        details: outdatedDeps
      });
    }

    // Check for known vulnerabilities
    const { stdout: vulnerabilities } = await execAsync('npm audit');
    if (vulnerabilities.includes('found')) {
      results.checks.push({
        type: 'vulnerabilities',
        status: 'warning',
        message: 'Security vulnerabilities found',
        details: vulnerabilities
      });
    }

    // Check file permissions
    const criticalFiles = [
      path.join(__dirname, '../.env'),
      path.join(__dirname, '../config/database.js'),
      path.join(__dirname, '../security/automated-security.js')
    ];

    for (const file of criticalFiles) {
      if (fs.existsSync(file)) {
        const stats = fs.statSync(file);
        const permissions = stats.mode.toString(8).slice(-3);
        if (parseInt(permissions) > 644) {
          results.checks.push({
            type: 'permissions',
            status: 'warning',
            message: `File permissions too permissive: ${file}`,
            details: `Current permissions: ${permissions}`
          });
        }
      }
    }

    // Check database security
    const [dbUsers] = await pool.query('SELECT user, host FROM mysql.user');
    for (const user of dbUsers) {
      if (user.host === '%') {
        results.checks.push({
          type: 'database',
          status: 'warning',
          message: 'Database user with wildcard host found',
          details: `User: ${user.user}, Host: ${user.host}`
        });
      }
    }

    // Log security check results
    logger.info('Security check completed:', results);

    return results;
  } catch (error) {
    logger.error('Security check failed:', error);
    throw error;
  }
}

// Run security check if script is executed directly
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  checkSecurity()
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}

export default securityMonitor;
