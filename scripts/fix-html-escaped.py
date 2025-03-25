import os
import html

def fix_html_files():
    # Walk through all directories recursively
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Unescape HTML entities
                content = html.unescape(content)
                
                # Write the fixed content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed {file_path}")

if __name__ == '__main__':
    fix_html_files() 