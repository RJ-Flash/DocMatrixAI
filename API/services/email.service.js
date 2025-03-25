const nodemailer = require('nodemailer');
const logger = require('../utils/logger');

class EmailService {
    static transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port: process.env.SMTP_PORT,
        secure: process.env.SMTP_PORT === '465',
        auth: {
            user: process.env.SMTP_USER,
            pass: process.env.SMTP_PASS
        }
    });

    static async sendVerificationEmail(email, token) {
        const verificationUrl = `${process.env.FRONTEND_URL}/verify-email?token=${token}`;
        
        const message = {
            from: process.env.FROM_EMAIL,
            to: email,
            subject: 'Verify your DocMatrix AI account',
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <img src="${process.env.FRONTEND_URL}/logo.png" alt="DocMatrix AI" style="max-width: 200px; margin: 20px 0;">
                    <h1 style="color: #2563eb;">Welcome to DocMatrix AI!</h1>
                    <p>Thank you for registering. Please verify your email address to activate your account.</p>
                    <a href="${verificationUrl}" style="display: inline-block; background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 20px 0;">
                        Verify Email
                    </a>
                    <p style="color: #666;">If the button doesn't work, copy and paste this link into your browser:</p>
                    <p style="color: #666;">${verificationUrl}</p>
                    <p style="color: #666;">This link will expire in 24 hours.</p>
                    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="color: #666; font-size: 12px;">
                        If you didn't create an account with DocMatrix AI, please ignore this email.
                    </p>
                </div>
            `
        };

        try {
            await this.transporter.sendMail(message);
            logger.info(`Verification email sent to ${email}`);
        } catch (error) {
            logger.error('Failed to send verification email:', error);
            throw error;
        }
    }

    static async sendPasswordResetEmail(email, token) {
        const resetUrl = `${process.env.FRONTEND_URL}/reset-password?token=${token}`;
        
        const message = {
            from: process.env.FROM_EMAIL,
            to: email,
            subject: 'Reset your DocMatrix AI password',
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <img src="${process.env.FRONTEND_URL}/logo.png" alt="DocMatrix AI" style="max-width: 200px; margin: 20px 0;">
                    <h1 style="color: #2563eb;">Password Reset Request</h1>
                    <p>We received a request to reset your password. Click the button below to choose a new password:</p>
                    <a href="${resetUrl}" style="display: inline-block; background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; margin: 20px 0;">
                        Reset Password
                    </a>
                    <p style="color: #666;">If the button doesn't work, copy and paste this link into your browser:</p>
                    <p style="color: #666;">${resetUrl}</p>
                    <p style="color: #666;">This link will expire in 1 hour.</p>
                    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="color: #666; font-size: 12px;">
                        If you didn't request a password reset, please ignore this email or contact support if you're concerned.
                    </p>
                </div>
            `
        };

        try {
            await this.transporter.sendMail(message);
            logger.info(`Password reset email sent to ${email}`);
        } catch (error) {
            logger.error('Failed to send password reset email:', error);
            throw error;
        }
    }

    static async sendWelcomeEmail(email, name) {
        const message = {
            from: process.env.FROM_EMAIL,
            to: email,
            subject: 'Welcome to DocMatrix AI!',
            html: `
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <img src="${process.env.FRONTEND_URL}/logo.png" alt="DocMatrix AI" style="max-width: 200px; margin: 20px 0;">
                    <h1 style="color: #2563eb;">Welcome aboard, ${name}!</h1>
                    <p>Thank you for joining DocMatrix AI. We're excited to have you as part of our community!</p>
                    <h2 style="color: #2563eb; margin-top: 30px;">Getting Started</h2>
                    <ul style="color: #666; line-height: 1.6;">
                        <li>Visit our <a href="${process.env.FRONTEND_URL}/docs" style="color: #2563eb;">documentation</a> to learn more about our features</li>
                        <li>Check out our <a href="${process.env.FRONTEND_URL}/tutorials" style="color: #2563eb;">tutorials</a> for step-by-step guides</li>
                        <li>Join our <a href="${process.env.FRONTEND_URL}/community" style="color: #2563eb;">community</a> to connect with other users</li>
                    </ul>
                    <div style="background-color: #f3f4f6; padding: 20px; border-radius: 4px; margin: 20px 0;">
                        <p style="margin: 0; color: #666;">
                            Need help? Our support team is available 24/7 at 
                            <a href="mailto:support@docmatrixai.com" style="color: #2563eb;">support@docmatrixai.com</a>
                        </p>
                    </div>
                    <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                    <p style="color: #666; font-size: 12px;">
                        You're receiving this email because you created an account with DocMatrix AI.
                    </p>
                </div>
            `
        };

        try {
            await this.transporter.sendMail(message);
            logger.info(`Welcome email sent to ${email}`);
        } catch (error) {
            logger.error('Failed to send welcome email:', error);
            throw error;
        }
    }
}

module.exports = EmailService;
