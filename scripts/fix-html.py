import os
import re
from glob import glob

def fix_html_files():
    try:
        files = glob('**/*.html', recursive=True)
        
        for file in files:
            print(f'Processing {file}...')
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix self-closing tags
            content = re.sub(r'<(meta|link|hr|img|input|br)[^>]*[^/]>', 
                           lambda m: m.group().replace('>', ' />'), 
                           content)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed {file}')
        
        print('All HTML files have been fixed')
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    fix_html_files() 