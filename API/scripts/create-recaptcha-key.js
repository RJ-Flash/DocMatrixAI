const { RecaptchaEnterpriseServiceClient } = require('@google-cloud/recaptcha-enterprise');
require('dotenv').config();

async function createSiteKey() {
    try {
        const client = new RecaptchaEnterpriseServiceClient();
        const projectId = process.env.GOOGLE_CLOUD_PROJECT;
        const domainName = 'docmatrixai.com';

        // Configure web settings
        const webSettings = {
            allowedDomains: [domainName, 'api.docmatrixai.com'],
            allowAmpTraffic: false,
            integrationType: 'SCORE'
        };

        // Create the key
        const key = {
            displayName: 'DocMatrix AI reCAPTCHA Key',
            webSettings: webSettings,
            labels: {
                environment: process.env.NODE_ENV
            }
        };

        const request = {
            parent: `projects/${projectId}`,
            key: key
        };

        const [response] = await client.createKey(request);
        const siteKey = response.name.split('/').pop();
        
        console.log('reCAPTCHA Site Key created successfully!');
        console.log('Site Key:', siteKey);
        console.log('\nAdd these to your .env files:');
        console.log(`RECAPTCHA_SITE_KEY=${siteKey}`);
        
        return siteKey;
    } catch (error) {
        console.error('Error creating reCAPTCHA site key:', error);
        throw error;
    }
}

createSiteKey().catch(console.error);
