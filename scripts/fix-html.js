const fs = require('fs');
const path = require('path');
const { glob } = require('glob');

function unescapeHtml(content) {
    return content
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'");
}

function fixHtmlFiles() {
    try {
        const files = glob.sync('**/*.html', { ignore: ['node_modules/**', 'scripts/**'] });
        
        for (const file of files) {
            console.log(`Processing ${file}...`);
            let content = fs.readFileSync(file, 'utf8');
            
            // First unescape any double-escaped content
            content = unescapeHtml(content);
            
            // Fix self-closing tags
            content = content.replace(/<(meta|link|hr|img|input|br)([^>]*?)(?<!\/)\s*>/g, '<$1$2 />');
            
            // Fix ID values to use dashes
            content = content.replace(/id="([^"]+)"/g, (match, id) => {
                const newId = id.toLowerCase().replace(/([a-z])([A-Z])/g, '$1-$2');
                return `id="${newId}"`;
            });
            
            // Fix class values to use dashes
            content = content.replace(/class="([^"]+)"/g, (match, classes) => {
                const newClasses = classes.split(' ')
                    .map(cls => cls.toLowerCase().replace(/([a-z])([A-Z])/g, '$1-$2'))
                    .join(' ');
                return `class="${newClasses}"`;
            });
            
            fs.writeFileSync(file, content, 'utf8');
            console.log(`Fixed ${file}`);
        }
        
        console.log('All HTML files have been fixed');
    } catch (error) {
        console.error('Error:', error);
    }
}

fixHtmlFiles();
