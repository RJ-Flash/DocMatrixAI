import os
import re

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
                
                # Fix special characters
                content = content.replace('&', '&amp;')
                content = content.replace('>', '&gt;')
                content = content.replace('<', '&lt;')
                
                # Fix self-closing tags
                content = re.sub(r'<(meta|link|hr|img|input|br)([^>]*?)(?<!/)>', r'<\1\2 />', content)
                
                # Fix ID and class values
                def fix_attr_value(match):
                    attr = match.group(1)
                    value = match.group(2).lower()
                    # Convert camelCase to kebab-case
                    value = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', value)
                    # Replace spaces with dashes
                    value = re.sub(r'\s+', '-', value)
                    # Remove multiple dashes
                    value = re.sub(r'-+', '-', value)
                    # Remove leading/trailing dashes
                    value = value.strip('-')
                    return f'{attr}="{value}"'
                
                content = re.sub(r'(id|class)="([^"]+)"', fix_attr_value, content)
                
                # Write the fixed content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

if __name__ == '__main__':
    fix_html_files() 