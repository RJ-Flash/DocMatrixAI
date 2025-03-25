require('dotenv').config();
const db = require('../config/database');
const IPWhitelist = require('../config/ip-whitelist');
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

async function showMenu() {
    console.log('\nIP Whitelist Management');
    console.log('1. View Whitelist');
    console.log('2. Add IP');
    console.log('3. Remove IP');
    console.log('4. Exit');
    
    rl.question('\nSelect an option: ', async (answer) => {
        switch(answer) {
            case '1':
                await viewWhitelist();
                break;
            case '2':
                await addIP();
                break;
            case '3':
                await removeIP();
                break;
            case '4':
                rl.close();
                process.exit(0);
                break;
            default:
                console.log('Invalid option');
                showMenu();
        }
    });
}

async function viewWhitelist() {
    const whitelist = await IPWhitelist.getWhitelist();
    console.log('\nCurrent Whitelist:');
    console.log('----------------------------------------');
    whitelist.forEach(entry => {
        console.log(`IP: ${entry.ip_address}`);
        console.log(`Description: ${entry.description}`);
        console.log(`Expires: ${entry.expires_at || 'Never'}`);
        console.log('----------------------------------------');
    });
    showMenu();
}

async function addIP() {
    rl.question('Enter IP address: ', (ip) => {
        rl.question('Enter description: ', async (description) => {
            rl.question('Enter expiry date (YYYY-MM-DD or press enter for never): ', async (expires) => {
                const expiresAt = expires ? new Date(expires) : null;
                await IPWhitelist.addToWhitelist(ip, description, expiresAt);
                console.log(`Added ${ip} to whitelist`);
                showMenu();
            });
        });
    });
}

async function removeIP() {
    rl.question('Enter IP address to remove: ', async (ip) => {
        await IPWhitelist.removeFromWhitelist(ip);
        console.log(`Removed ${ip} from whitelist`);
        showMenu();
    });
}

// Start the menu
showMenu();
