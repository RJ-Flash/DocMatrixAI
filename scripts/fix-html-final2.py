import os
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
                    
                    # Remove extra spaces and line breaks
                    content = re.sub(r'\s+', ' ', content)
                    
                    # Fix self-closing tags
                    content = re.sub(r'<(meta|link|hr|img|input|br)([^>]*?)(?<!\/)\s*>', r'<\1\2 />', content)
                    
                    # Fix empty attributes
                    content = re.sub(r'\s+=""', '', content)
                    
                    # Fix doctype
                    content = re.sub(r'(?i)<!DOCTYPE\s+html\s*>', '<!DOCTYPE html>', content)
                    
                    # Add proper line breaks for readability
                    content = re.sub(r'>\s*<', '>\n<', content)
                    content = re.sub(r'(</(div|section|nav|footer|header|main|article|aside|form)>)', r'\1\n', content)
                    
                    # Write the fixed content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Fixed {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

if __name__ == '__main__':
    fix_html_files() 