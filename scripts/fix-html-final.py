import os
import html
import re

def fix_html_files():
    # Walk through all directories recursively
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                
                try:
                    # Read the file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Direct string replacements for common escaped sequences
                    content = content.replace('&lt;', '<')
                    content = content.replace('&gt;', '>')
                    content = content.replace('&amp;', '&')
                    content = content.replace('&quot;', '"')
                    content = content.replace('&#39;', "'")
                    
                    # Additional unescaping for any remaining HTML entities
                    content = html.unescape(content)
                    
                    # Write the fixed content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Fixed {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

if __name__ == '__main__':
    fix_html_files() 