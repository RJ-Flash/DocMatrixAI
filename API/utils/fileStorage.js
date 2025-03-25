const path = require('path');
const fs = require('fs').promises;
const multer = require('multer');
const logger = require('./logger');

class FileStorage {
    constructor() {
        this.storageType = process.env.STORAGE_TYPE || 'local';
        this.setupStorage();
    }

    setupStorage() {
        if (this.storageType === 'local') {
            this.storage = multer.diskStorage({
                destination: async (req, file, cb) => {
                    const uploadPath = path.join(process.env.UPLOAD_PATH, req.user.id.toString());
                    try {
                        await fs.mkdir(uploadPath, { recursive: true });
                        cb(null, uploadPath);
                    } catch (error) {
                        cb(error);
                    }
                },
                filename: (req, file, cb) => {
                    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
                    cb(null, uniqueSuffix + path.extname(file.originalname));
                }
            });
        } else if (this.storageType === 's3') {
            const AWS = require('aws-sdk');
            const multerS3 = require('multer-s3');

            const s3 = new AWS.S3({
                accessKeyId: process.env.AWS_ACCESS_KEY_ID,
                secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
                region: process.env.AWS_REGION
            });

            this.storage = multerS3({
                s3: s3,
                bucket: process.env.S3_BUCKET,
                metadata: (req, file, cb) => {
                    cb(null, { fieldName: file.fieldname });
                },
                key: (req, file, cb) => {
                    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
                    cb(null, `uploads/${req.user.id}/${uniqueSuffix}-${file.originalname}`);
                }
            });
        }
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
            if (this.storageType === 'local') {
                await fs.unlink(filePath);
            } else if (this.storageType === 's3') {
                const AWS = require('aws-sdk');
                const s3 = new AWS.S3({
                    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
                    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
                    region: process.env.AWS_REGION
                });

                await s3.deleteObject({
                    Bucket: process.env.S3_BUCKET,
                    Key: filePath
                }).promise();
            }
            logger.info(`File deleted successfully: ${filePath}`);
        } catch (error) {
            logger.error(`Error deleting file: ${filePath}`, error);
            throw error;
        }
    }
}

module.exports = new FileStorage();
