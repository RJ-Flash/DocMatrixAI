const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);
const glob = promisify(require('glob'));

async function fixHtmlFiles() {
    try {
        const files = await glob('**/*.html', { ignore: ['node_modules/**', 'scripts/**'] });
        
        for (const file of files) {
            console.log(`Processing ${file}...`);
            let content = await readFile(file, 'utf8');
            
            // Fix self-closing tags
            content = content.replace(/<(meta|link|hr|img|input|br)[^>]*[^/]>/g, match => {
                return match.replace(/\s*>$/, ' />');
            });
            
            await writeFile(file, content, 'utf8');
            console.log(`Fixed ${file}`);
        }
        
        console.log('All HTML files have been fixed');
    } catch (error) {
        console.error('Error:', error);
    }
}

fixHtmlFiles(); 