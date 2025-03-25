const nodemailer = require('nodemailer');
const logger = require('./logger');

const sendEmail = async (options) => {
    const transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST,
        port: process.env.SMTP_PORT,
        auth: {
            user: process.env.SMTP_USER,
            pass: process.env.SMTP_PASS
        }
    });

    const message = {
        from: `${process.env.EMAIL_FROM_NAME} <${process.env.EMAIL_FROM}>`,
        to: options.email,
        subject: options.subject,
        text: options.message
    };

    try {
        const info = await transporter.sendMail(message);
        logger.info('Email sent successfully', { messageId: info.messageId });
    } catch (error) {
        logger.error('Error sending email:', error);
        throw error;
    }
};

module.exports = sendEmail;
