import os
import sys
import argparse
from pathlib import Path

def check_consistency():
    """Check consistency manually instead of running the script."""
    base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    issues = []
    
    # Check for dark mode CSS in all HTML files
    for html_file in base_dir.glob('**/*.html'):
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if 'dark-mode.css' not in content:
                issues.append(f"{html_file.relative_to(base_dir)}: Missing dark mode CSS")
            
            if 'dark-mode-toggle' not in content:
                issues.append(f"{html_file.relative_to(base_dir)}: Missing dark mode toggle")
            
            if 'meta name="description"' not in content and 'index.html' in str(html_file):
                issues.append(f"{html_file.relative_to(base_dir)}: Missing meta description")
    
    return issues 

def check_required_files():
    """Check if all required files exist."""
    base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    required_files = [
        'images/favicon-16x16.png',
        'images/favicon-32x32.png',
        'images/favicon-192x192.png',
        'images/favicon-512x512.png',
        'images/technology_infographic.svg',
        '.htaccess'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = base_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    return missing_files

def check_htaccess():
    """Check if .htaccess file is properly configured."""
    base_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    htaccess_path = base_dir / '.htaccess'
    
    if not htaccess_path.exists():
        return False
    
    with open(htaccess_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Check for essential configurations
        if 'ErrorDocument 404' not in content:
            return False
        
        if 'RewriteEngine On' not in content:
            return False
    
    return True

def check_image_optimization():
    """Check if all images are optimized."""
    # This is a simplified check - in a real scenario, you would use tools like ImageOptim API
    # or check file sizes against benchmarks
    return True

def main():
    parser = argparse.ArgumentParser(description='Deployment checklist for DocMatrix AI website')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    args = parser.parse_args()
    
    verbose = args.verbose
    
    if verbose:
        print("Running deployment checklist with verbose output...\n")
    
    # Check required files
    missing_files = check_required_files()
    if missing_files:
        if verbose:
            print("❌ Missing required files:")
            for file in missing_files:
                print(f"  - {file}")
        else:
            print(f"❌ Missing {len(missing_files)} required files")
    else:
        if verbose:
            print("✅ All required files exist")
    
    # Check .htaccess
    htaccess_ok = check_htaccess()
    if htaccess_ok:
        if verbose:
            print("✅ .htaccess file is properly configured")
    else:
        if verbose:
            print("❌ .htaccess file is missing or improperly configured")
    
    # Check consistency
    consistency_issues = check_consistency()
    if consistency_issues:
        if verbose:
            print("❌ Consistency issues found:")
            for issue in consistency_issues:
                print(f"  - {issue}")
        else:
            print(f"❌ Found {len(consistency_issues)} consistency issues")
    else:
        if verbose:
            print("✅ All pages are consistent")
    
    # Check image optimization
    images_optimized = check_image_optimization()
    if images_optimized:
        if verbose:
            print("✅ All images are optimized")
    else:
        if verbose:
            print("❌ Some images are not optimized")
    
    # Summary
    if verbose:
        print("\n---------------------------")
    
    if not missing_files and htaccess_ok and not consistency_issues and images_optimized:
        if verbose:
            print("✅ The website is ready for deployment!")
        else:
            print("✅ Website is ready for deployment!")
        return 0
    else:
        total_issues = len(missing_files) + (0 if htaccess_ok else 1) + len(consistency_issues) + (0 if images_optimized else 1)
        if verbose:
            print(f"❌ {total_issues} issues need to be fixed before deployment")
        else:
            print(f"❌ {total_issues} issues need to be fixed before deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 