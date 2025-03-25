const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);
const glob = promisify(require('glob'));

async function fixHtmlFiles() {
    try {
        const files = await glob('**/*.html');
        
        for (const file of files) {
            let content = await readFile(file, 'utf8');
            
            // Fix self-closing tags
            content = content.replace(/<(meta|link|hr|img|input|br)[^>]*[^/]>/g, match => {
                return match.replace(/\s*>$/, ' />');
            });
            
            // Fix special characters
            content = content.replace(/&(?!amp;|lt;|gt;|quot;|#)/g, '&amp;');
            content = content.replace(/>/g, '&gt;');
            content = content.replace(/</g, '&lt;');
            
            // Fix ID values to use dashes
            content = content.replace(/id="([^"]+)"/g, (match, id) => {
                const newId = id.toLowerCase().replace(/([a-z])([A-Z])/g, '$1-$2');
                return `id="${newId}"`;
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