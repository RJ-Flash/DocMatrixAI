# DocMatrix AI Website Deployment Guide

This guide provides instructions for deploying the DocMatrix AI website to staging and production environments.

## Prerequisites

- Access to HostGator hosting account
- FTP client (e.g., FileZilla)
- Basic knowledge of HTML, CSS, and JavaScript

## Website Structure

The DocMatrix AI website consists of the following key components:

- HTML pages for all sections (main page, products, about, careers, etc.)
- CSS stylesheets in the `css/` directory
- JavaScript files in the `js/` directory
- Images in the `images/` directory
- `.htaccess` file for server configuration

## Pre-Deployment Checklist

Before deploying, ensure the following:

1. **Run the consistency verification script**:
   ```
   python scripts/verify_consistency.py
   ```
   This script checks for consistency in dark mode support, navigation, URLs, and meta tags.

2. **Run the deployment checklist script**:
   ```
   python scripts/deployment_checklist.py
   ```
   This script verifies that all required files exist and are properly configured.

3. **Generate the technology image**:
   ```
   python scripts/generate_tech_image.py
   ```
   This script generates the dynamic technology image used in the Technology section.

4. **Manually verify**:
   - All links work correctly
   - Dark/light mode toggle functions properly
   - Images load correctly
   - Forms submit properly
   - Responsive design works on different screen sizes

## Staging Deployment

1. **Create a staging subdomain** (e.g., staging.docmatrixai.com) in your HostGator control panel.

2. **Upload the website files**:
   - Connect to the staging server using FTP
   - Upload all files and directories from the `docmatrixai_com/` directory to the staging server's root directory
   - Ensure file permissions are set correctly (typically 644 for files and 755 for directories)

3. **Test the staging website**:
   - Verify all pages load correctly
   - Test navigation and links
   - Test dark/light mode toggle
   - Test responsive design on different devices
   - Verify forms and interactive elements work as expected

## Production Deployment

Once the staging deployment has been thoroughly tested and approved:

1. **Backup the existing production website** (if applicable).

2. **Upload the website files**:
   - Connect to the production server using FTP
   - Upload all files and directories from the `docmatrixai_com/` directory to the production server's root directory
   - Ensure file permissions are set correctly (typically 644 for files and 755 for directories)

3. **Verify the production website**:
   - Check that all pages load correctly
   - Verify that all links work
   - Test the dark/light mode toggle
   - Test on different browsers and devices

## Post-Deployment Tasks

After successful deployment:

1. **Monitor website performance** using tools like Google Analytics and Google Search Console.

2. **Check for any 404 errors** or broken links using tools like Google Search Console.

3. **Verify SEO elements** are correctly implemented and indexed by search engines.

4. **Test website speed** using tools like Google PageSpeed Insights and make optimizations if necessary.

## Troubleshooting

If you encounter issues during deployment:

1. **Check server logs** for any error messages.

2. **Verify file permissions** are set correctly.

3. **Check for syntax errors** in the `.htaccess` file.

4. **Test in different browsers** to identify browser-specific issues.

5. **Verify that all required files** were uploaded successfully.

## Maintenance

Regular maintenance tasks include:

1. **Updating content** as needed.

2. **Monitoring website performance** and making optimizations.

3. **Checking for broken links** and fixing them promptly.

4. **Keeping dependencies updated** (e.g., Bootstrap, jQuery).

5. **Backing up the website** regularly.

## Contact

For questions or assistance with deployment, contact the development team at [dev@docmatrixai.com](mailto:dev@docmatrixai.com). 