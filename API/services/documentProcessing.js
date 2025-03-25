const AWS = require('aws-sdk');
const { Configuration, OpenAIApi } = require('openai');
const logger = require('../utils/logger');

// Configure OpenAI
const configuration = new Configuration({
    apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

// Configure AWS Textract
const textract = new AWS.Textract();

async function extractTextFromDocument(s3Key) {
    const params = {
        Document: {
            S3Object: {
                Bucket: process.env.S3_BUCKET,
                Name: s3Key
            }
        }
    };

    const result = await textract.detectDocumentText(params).promise();
    return result.Blocks
        .filter(block => block.BlockType === 'LINE')
        .map(block => block.Text)
        .join(' ');
}

async function analyzeWithGPT(text, prompt) {
    const response = await openai.createCompletion({
        model: "gpt-4",
        prompt: `${prompt}\n\nDocument text:\n${text}`,
        max_tokens: 1000,
        temperature: 0.3
    });

    return response.data.choices[0].text.trim();
}

// Process Contract Documents
async function processContractDocument(document) {
    const text = await extractTextFromDocument(document.s3Key);
    
    const prompt = `Analyze this contract and extract the following information:
    1. Contract parties
    2. Key dates (start date, end date, etc.)
    3. Contract value
    4. Key terms and conditions
    5. Obligations of each party
    6. Termination clauses
    Format the response as a JSON object.`;

    const analysis = await analyzeWithGPT(text, prompt);
    return JSON.parse(analysis);
}

// Process Expense Documents
async function processExpenseDocument(document) {
    const text = await extractTextFromDocument(document.s3Key);
    
    const prompt = `Analyze this expense document and extract the following information:
    1. Total amount
    2. Date of expense
    3. Vendor/Merchant name
    4. Category of expense
    5. Individual line items with amounts
    6. Tax amount if applicable
    Format the response as a JSON object.`;

    const analysis = await analyzeWithGPT(text, prompt);
    return JSON.parse(analysis);
}

// Process HR Documents
async function processHRDocument(document) {
    const text = await extractTextFromDocument(document.s3Key);
    
    const prompt = `Analyze this HR document and extract the following information:
    1. Document type (resume, offer letter, performance review, etc.)
    2. Key personnel information
    3. Dates mentioned
    4. Important terms or conditions
    5. Action items or next steps
    Format the response as a JSON object.`;

    const analysis = await analyzeWithGPT(text, prompt);
    return JSON.parse(analysis);
}

// Process Supply Chain Documents
async function processSupplyDocument(document) {
    const text = await extractTextFromDocument(document.s3Key);
    
    const prompt = `Analyze this supply chain document and extract the following information:
    1. Document type (purchase order, invoice, shipping manifest, etc.)
    2. Supplier and buyer information
    3. Order details (items, quantities, prices)
    4. Delivery terms and dates
    5. Payment terms
    Format the response as a JSON object.`;

    const analysis = await analyzeWithGPT(text, prompt);
    return JSON.parse(analysis);
}

module.exports = {
    processContractDocument,
    processExpenseDocument,
    processHRDocument,
    processSupplyDocument
};
