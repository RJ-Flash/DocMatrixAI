import os

def fix_html_files():
    replacements = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&quot;': '"',
        '&#39;': "'"
    }
    
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
                    
                    # Replace escaped entities
                    for escaped, unescaped in replacements.items():
                        content = content.replace(escaped, unescaped)
                    
                    # Write the fixed content back to the file
                    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(content)
                    print(f"Fixed {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

if __name__ == '__main__':
    fix_html_files() 