const crypto = require('crypto');
const User = require('../models/User');
const ErrorResponse = require('../utils/errorResponse');
const sendEmail = require('../utils/sendEmail');
const asyncHandler = require('../middleware/async');
const jwt = require('jsonwebtoken');

// @desc    Register user
// @route   POST /api/v1/auth/register
// @access  Public
exports.register = asyncHandler(async (req, res, next) => {
    const { name, email, password } = req.body;

    // Create verification token
    const verificationToken = crypto.randomBytes(20).toString('hex');
    const verificationExpire = Date.now() + 24 * 60 * 60 * 1000; // 24 hours

    // Create user
    const user = await User.create({
        name,
        email,
        password,
        verificationToken,
        verificationExpire
    });

    // Send verification email
    const verificationUrl = `${process.env.CORS_ORIGIN}/verify-email/${verificationToken}`;
    const message = `Please verify your email by clicking on this link: ${verificationUrl}`;

    try {
        await sendEmail({
            email: user.email,
            subject: 'Email Verification',
            message
        });

        sendTokenResponse(user, 200, res);
    } catch (err) {
        user.verificationToken = undefined;
        user.verificationExpire = undefined;
        await user.save();

        return next(new ErrorResponse('Email could not be sent', 500));
    }
});

// @desc    Login user
// @route   POST /api/v1/auth/login
// @access  Public
exports.login = asyncHandler(async (req, res, next) => {
    const { email, password } = req.body;

    // Validate email & password
    if (!email || !password) {
        return next(new ErrorResponse('Please provide an email and password', 400));
    }

    // Check for user
    const user = await User.findOne({ email }).select('+password');
    if (!user) {
        return next(new ErrorResponse('Invalid credentials', 401));
    }

    // Check if password matches
    const isMatch = await user.matchPassword(password);
    if (!isMatch) {
        return next(new ErrorResponse('Invalid credentials', 401));
    }

    // Check if email is verified
    if (!user.isVerified) {
        return next(new ErrorResponse('Please verify your email to login', 401));
    }

    sendTokenResponse(user, 200, res);
});

// @desc    Verify email
// @route   GET /api/v1/auth/verify-email/:token
// @access  Public
exports.verifyEmail = asyncHandler(async (req, res, next) => {
    const user = await User.findOne({
        verificationToken: req.params.token,
        verificationExpire: { $gt: Date.now() }
    });

    if (!user) {
        return next(new ErrorResponse('Invalid verification token', 400));
    }

    // Update user
    user.isVerified = true;
    user.verificationToken = undefined;
    user.verificationExpire = undefined;
    await user.save();

    res.status(200).json({
        success: true,
        message: 'Email verified successfully'
    });
});

// Helper function to get token from model, create cookie and send response
const sendTokenResponse = (user, statusCode, res) => {
    // Create token
    const token = user.getSignedJwtToken();

    const options = {
        expires: new Date(Date.now() + process.env.JWT_COOKIE_EXPIRE * 24 * 60 * 60 * 1000),
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production'
    };

    res
        .status(statusCode)
        .cookie('token', token, options)
        .json({
            success: true,
            token
        });
};
