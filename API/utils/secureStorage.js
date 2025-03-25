const path = require('path');
const fs = require('fs').promises;
const crypto = require('crypto');
const multer = require('multer');
const logger = require('./logger');

class SecureStorage {
    constructor() {
        // Use Hostgator's secure directory outside public_html
        this.baseUploadPath = process.env.UPLOAD_PATH || '../secure_uploads';
        this.algorithm = 'aes-256-gcm';
        this.setupStorage();
    }

    setupStorage() {
        this.storage = multer.diskStorage({
            destination: async (req, file, cb) => {
                // Create user-specific encrypted directory
                const userHash = this.hashString(req.user.id.toString());
                const uploadPath = path.join(this.baseUploadPath, userHash);
                try {
                    await fs.mkdir(uploadPath, { recursive: true, mode: 0o700 }); // Only owner can read/write
                    await fs.chmod(uploadPath, 0o700); // Ensure permissions
                    cb(null, uploadPath);
                } catch (error) {
                    cb(error);
                }
            },
            filename: (req, file, cb) => {
                // Generate encrypted filename
                const timestamp = Date.now();
                const random = Math.round(Math.random() * 1E9);
                const originalExt = path.extname(file.originalname);
                const encryptedName = this.encryptString(`${timestamp}-${random}${originalExt}`);
                cb(null, encryptedName);
            }
        });
    }

    // Encrypt file contents
    async encryptFile(filePath) {
        const fileKey = crypto.randomBytes(32);
        const iv = crypto.randomBytes(12);
        const cipher = crypto.createCipheriv(this.algorithm, fileKey, iv);
        
        const fileContent = await fs.readFile(filePath);
        const encrypted = Buffer.concat([cipher.update(fileContent), cipher.final()]);
        const authTag = cipher.getAuthTag();

        // Save encryption metadata separately
        const metaPath = filePath + '.meta';
        await fs.writeFile(metaPath, JSON.stringify({
            key: fileKey.toString('hex'),
            iv: iv.toString('hex'),
            authTag: authTag.toString('hex')
        }));

        // Save encrypted content
        await fs.writeFile(filePath, encrypted);
        await fs.chmod(filePath, 0o600); // Only owner can read/write
        await fs.chmod(metaPath, 0o600);

        return {
            encryptedPath: filePath,
            metaPath: metaPath
        };
    }

    // Decrypt file contents
    async decryptFile(filePath) {
        const metaPath = filePath + '.meta';
        const meta = JSON.parse(await fs.readFile(metaPath, 'utf8'));
        const fileKey = Buffer.from(meta.key, 'hex');
        const iv = Buffer.from(meta.iv, 'hex');
        const authTag = Buffer.from(meta.authTag, 'hex');

        const decipher = crypto.createDecipheriv(this.algorithm, fileKey, iv);
        decipher.setAuthTag(authTag);

        const encrypted = await fs.readFile(filePath);
        const decrypted = Buffer.concat([decipher.update(encrypted), decipher.final()]);
        
        return decrypted;
    }

    // Hash string (for directory names)
    hashString(str) {
        return crypto
            .createHash('sha256')
            .update(str)
            .digest('hex');
    }

    // Encrypt string (for filenames)
    encryptString(str) {
        const key = crypto.scryptSync(process.env.FILE_ENCRYPTION_KEY, 'salt', 32);
        const iv = crypto.randomBytes(12);
        const cipher = crypto.createCipheriv(this.algorithm, key, iv);
        const encrypted = cipher.update(str, 'utf8', 'hex') + cipher.final('hex');
        const authTag = cipher.getAuthTag();
        return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
    }

    getUpload() {
        return multer({
            storage: this.storage,
            fileFilter: (req, file, cb) => {
                const filetypes = /pdf|doc|docx|xls|xlsx/;
                const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
                const mimetype = filetypes.test(file.mimetype);

                if (mimetype && extname) {
                    return cb(null, true);
                }
                cb(new Error('Only PDF, DOC, DOCX, XLS, XLSX files are allowed!'));
            },
            limits: {
                fileSize: 10 * 1024 * 1024 // 10MB
            }
        }).single('document');
    }

    async deleteFile(filePath) {
        try {
            await fs.unlink(filePath);
            const metaPath = filePath + '.meta';
            await fs.unlink(metaPath).catch(() => {}); // Delete metadata if exists
            logger.info(`File and metadata deleted successfully: ${filePath}`);
        } catch (error) {
            logger.error(`Error deleting file: ${filePath}`, error);
            throw error;
        }
    }
}

module.exports = new SecureStorage();
