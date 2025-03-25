const AWS = require('aws-sdk');
const multer = require('multer');
const multerS3 = require('multer-s3');
const path = require('path');
const Document = require('../models/Document');
const ErrorResponse = require('../utils/errorResponse');
const asyncHandler = require('../middleware/async');
const logger = require('../utils/logger');

// Configure AWS
AWS.config.update({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGION
});

const s3 = new AWS.S3();

// Configure multer for S3 upload
const upload = multer({
    storage: multerS3({
        s3: s3,
        bucket: process.env.S3_BUCKET,
        metadata: function (req, file, cb) {
            cb(null, { fieldName: file.fieldname });
        },
        key: function (req, file, cb) {
            const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
            cb(null, `uploads/${req.user.id}/${uniqueSuffix}-${file.originalname}`);
        }
    }),
    fileFilter: function(req, file, cb) {
        const filetypes = /pdf|doc|docx|xls|xlsx/;
        const extname = filetypes.test(path.extname(file.originalname).toLowerCase());
        const mimetype = filetypes.test(file.mimetype);

        if (mimetype && extname) {
            return cb(null, true);
        }
        cb(new Error('Error: Only PDF, DOC, DOCX, XLS, XLSX files are allowed!'));
    },
    limits: {
        fileSize: parseInt(process.env.MAX_FILE_SIZE) || 10485760 // 10MB default
    }
}).single('document');

// @desc    Upload document
// @route   POST /api/v1/documents
// @access  Private
exports.uploadDocument = asyncHandler(async (req, res, next) => {
    upload(req, res, async function(err) {
        if (err) {
            return next(new ErrorResponse(err.message, 400));
        }

        if (!req.file) {
            return next(new ErrorResponse('Please upload a file', 400));
        }

        const document = await Document.create({
            name: req.body.name || req.file.originalname,
            originalName: req.file.originalname,
            mimeType: req.file.mimetype,
            size: req.file.size,
            path: req.file.location,
            s3Key: req.file.key,
            processingType: req.body.processingType,
            user: req.user.id
        });

        res.status(201).json({
            success: true,
            data: document
        });
    });
});

// @desc    Get all documents
// @route   GET /api/v1/documents
// @access  Private
exports.getDocuments = asyncHandler(async (req, res, next) => {
    const documents = await Document.find({ user: req.user.id });

    res.status(200).json({
        success: true,
        count: documents.length,
        data: documents
    });
});

// @desc    Get single document
// @route   GET /api/v1/documents/:id
// @access  Private
exports.getDocument = asyncHandler(async (req, res, next) => {
    const document = await Document.findById(req.params.id);

    if (!document) {
        return next(new ErrorResponse('Document not found', 404));
    }

    // Make sure user owns document
    if (document.user.toString() !== req.user.id) {
        return next(new ErrorResponse('Not authorized to access this document', 401));
    }

    res.status(200).json({
        success: true,
        data: document
    });
});

// @desc    Delete document
// @route   DELETE /api/v1/documents/:id
// @access  Private
exports.deleteDocument = asyncHandler(async (req, res, next) => {
    const document = await Document.findById(req.params.id);

    if (!document) {
        return next(new ErrorResponse('Document not found', 404));
    }

    // Make sure user owns document
    if (document.user.toString() !== req.user.id) {
        return next(new ErrorResponse('Not authorized to delete this document', 401));
    }

    // Delete from S3
    await s3.deleteObject({
        Bucket: process.env.S3_BUCKET,
        Key: document.s3Key
    }).promise();

    await document.remove();

    res.status(200).json({
        success: true,
        data: {}
    });
});

// @desc    Process document
// @route   POST /api/v1/documents/:id/process
// @access  Private
exports.processDocument = asyncHandler(async (req, res, next) => {
    const document = await Document.findById(req.params.id);

    if (!document) {
        return next(new ErrorResponse('Document not found', 404));
    }

    // Make sure user owns document
    if (document.user.toString() !== req.user.id) {
        return next(new ErrorResponse('Not authorized to process this document', 401));
    }

    // Update status to processing
    document.status = 'processing';
    await document.save();

    // Process document based on type
    try {
        let result;
        switch (document.processingType) {
            case 'contract':
                result = await processContractDocument(document);
                break;
            case 'expense':
                result = await processExpenseDocument(document);
                break;
            case 'hr':
                result = await processHRDocument(document);
                break;
            case 'supply':
                result = await processSupplyDocument(document);
                break;
            default:
                throw new Error('Invalid processing type');
        }

        // Update document with results
        document.status = 'completed';
        document.metadata = result;
        await document.save();

        res.status(200).json({
            success: true,
            data: document
        });
    } catch (err) {
        document.status = 'failed';
        document.metadata = { error: err.message };
        await document.save();

        return next(new ErrorResponse('Document processing failed', 500));
    }
});
