#!/usr/bin/env python3
"""
Favicon Generator for DocMatrix AI

This script generates favicon files in different sizes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def generate_favicon(size):
    """Generate a simple favicon with the letter 'D' in the DocMatrix AI color."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a rounded rectangle background
    radius = size // 4
    draw.rounded_rectangle([(0, 0), (size, size)], radius, fill=(108, 92, 231))
    
    # Try to add a "D" in the center if size allows
    if size >= 16:
        try:
            # Use a default font if custom font is not available
            font_size = size // 2
            font = ImageFont.truetype("arial.ttf", font_size)
            
            # Calculate text position to center it
            try:
                # For newer Pillow versions
                left, top, right, bottom = draw.textbbox((0, 0), "D", font=font)
                text_width = right - left
                text_height = bottom - top
            except AttributeError:
                # For older Pillow versions
                text_width, text_height = draw.textsize("D", font=font)
                
            position = ((size - text_width) // 2, (size - text_height) // 2 - font_size // 4)
            
            # Draw the text
            draw.text(position, "D", fill=(255, 255, 255), font=font)
        except Exception:
            # If font rendering fails, just use the colored square
            pass
    
    return img

def main():
    """Generate favicon files in different sizes."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "images")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate favicons in different sizes
    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "favicon-192x192.png": 192,
        "favicon-512x512.png": 512
    }
    
    for filename, size in sizes.items():
        favicon = generate_favicon(size)
        output_path = os.path.join(output_dir, filename)
        favicon.save(output_path)
        print(f"Generated {filename} ({size}x{size})")

if __name__ == "__main__":
    main() 