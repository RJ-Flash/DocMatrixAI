const { RecaptchaEnterpriseServiceClient } = require('@google-cloud/recaptcha-enterprise');
const logger = require('./logger');

class RecaptchaService {
    constructor() {
        this.client = new RecaptchaEnterpriseServiceClient();
        this.projectId = process.env.GOOGLE_CLOUD_PROJECT;
        this.siteKey = process.env.RECAPTCHA_SITE_KEY;
    }

    async createAssessment(token, action) {
        try {
            const projectPath = this.client.projectPath(this.projectId);
            
            const request = {
                parent: projectPath,
                assessment: {
                    event: {
                        token: token,
                        siteKey: this.siteKey,
                        expectedAction: action
                    }
                }
            };

            const [assessment] = await this.client.createAssessment(request);
            
            if (!assessment.tokenProperties.valid) {
                logger.error('The CreateAssessment call failed because the token was invalid.');
                return {
                    success: false,
                    score: 0,
                    reason: 'Invalid token'
                };
            }

            if (assessment.tokenProperties.action !== action) {
                logger.error(`The action attribute in the reCAPTCHA token doesn't match the expected action.`);
                return {
                    success: false,
                    score: 0,
                    reason: 'Action mismatch'
                };
            }

            const score = assessment.riskAnalysis.score;
            logger.info(`Assessment score: ${score}`);

            return {
                success: true,
                score: score,
                reason: score >= 0.5 ? 'Passed' : 'Score too low'
            };

        } catch (error) {
            logger.error('Error creating reCAPTCHA assessment:', error);
            return {
                success: false,
                score: 0,
                reason: 'Assessment failed'
            };
        }
    }

    async verifyToken(token, action, minScore = 0.5) {
        const assessment = await this.createAssessment(token, action);
        return {
            ...assessment,
            passed: assessment.success && assessment.score >= minScore
        };
    }
}

module.exports = new RecaptchaService();
