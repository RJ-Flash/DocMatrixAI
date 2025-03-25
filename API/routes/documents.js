const express = require('express');
const router = express.Router();
const { protect } = require('../middleware/auth');
const {
    uploadDocument,
    getDocuments,
    getDocument,
    deleteDocument,
    processDocument
} = require('../controllers/documents');

// Protect all routes
router.use(protect);

router.route('/')
    .post(uploadDocument)
    .get(getDocuments);

router.route('/:id')
    .get(getDocument)
    .delete(deleteDocument);

router.post('/:id/process', processDocument);

module.exports = router;
