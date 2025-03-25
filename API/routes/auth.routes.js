const express = require('express');
const { body } = require('express-validator');
const rateLimit = require('express-rate-limit');
const AuthService = require('../services/auth.service');
const validate = require('../middleware/validate');
const { asyncHandler } = require('../utils/async-handler');

const router = express.Router();

// Rate limiting
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 attempts
    message: { error: 'Too many login attempts. Please try again later.' }
});

const registrationLimiter = rateLimit({
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 3, // 3 attempts
    message: { error: 'Too many registration attempts. Please try again later.' }
});

// Registration
router.post(
    '/register',
    registrationLimiter,
    [
        body('name').trim().notEmpty().withMessage('Name is required'),
        body('email').isEmail().withMessage('Invalid email address'),
        body('password')
            .isLength({ min: 8 })
            .withMessage('Password must be at least 8 characters long')
            .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
            .withMessage('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character'),
        body('company').optional().trim()
    ],
    validate,
    asyncHandler(async (req, res) => {
        const result = await AuthService.register({
            ...req.body,
            ip: req.ip,
            userAgent: req.get('user-agent')
        });
        res.json(result);
    })
);

// Login
router.post(
    '/login',
    loginLimiter,
    [
        body('email').isEmail().withMessage('Invalid email address'),
        body('password').notEmpty().withMessage('Password is required')
    ],
    validate,
    asyncHandler(async (req, res) => {
        const { email, password } = req.body;
        const result = await AuthService.login(
            email,
            password,
            req.ip,
            req.get('user-agent')
        );
        res.json(result);
    })
);

// Email verification
router.get(
    '/verify-email/:token',
    asyncHandler(async (req, res) => {
        const result = await AuthService.verifyEmail(req.params.token);
        res.json(result);
    })
);

// Password reset request
router.post(
    '/reset-password-request',
    [
        body('email').isEmail().withMessage('Invalid email address')
    ],
    validate,
    asyncHandler(async (req, res) => {
        const result = await AuthService.requestPasswordReset(req.body.email);
        res.json(result);
    })
);

// Password reset
router.post(
    '/reset-password',
    [
        body('token').notEmpty().withMessage('Token is required'),
        body('password')
            .isLength({ min: 8 })
            .withMessage('Password must be at least 8 characters long')
            .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)
            .withMessage('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character')
    ],
    validate,
    asyncHandler(async (req, res) => {
        const result = await AuthService.resetPassword(
            req.body.token,
            req.body.password
        );
        res.json(result);
    })
);

// Token refresh
router.post(
    '/refresh-token',
    [
        body('refreshToken').notEmpty().withMessage('Refresh token is required')
    ],
    validate,
    asyncHandler(async (req, res) => {
        const result = await AuthService.refreshToken(req.body.refreshToken);
        res.json(result);
    })
);

module.exports = router;
