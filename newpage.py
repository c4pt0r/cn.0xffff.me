#!/usr/bin/env python3
"""
Generate cfg and html files from markdown file.
Usage: python generate_page.py input.md
"""

import sys
import os
import re
from pathlib import Path
import markdown2
from datetime import date
import argparse

def extract_title_from_md(md_content: str) -> str:
    """Extract the first h1 title from markdown content."""
    # Look for the first # header
    match = re.search(r'^\s*#\s+(.+)$', md_content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""

def get_next_number(pages_dir: Path) -> str:
    """Get the next available number for the page."""
    if not pages_dir.exists():
        pages_dir.mkdir(parents=True)
        return "001"
    
    # Find all cfg files and get the highest number
    cfg_files = list(pages_dir.glob("*.cfg"))
    if not cfg_files:
        return "001"
    
    numbers = [int(f.name[:3]) for f in cfg_files if f.name[:3].isdigit()]
    if not numbers:
        return "001"
    
    return f"{max(numbers) + 1:03d}"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to be URL-friendly."""
    # Convert to lowercase and replace spaces/special chars with hyphens
    clean = re.sub(r'[^a-z0-9]+', '-', filename.lower())
    # Remove leading/trailing hyphens
    clean = clean.strip('-')
    # Remove consecutive hyphens
    clean = re.sub(r'-+', '-', clean)
    return clean

def create_cfg_file(cfg_path: Path, html_filename: str, title: str) -> None:
    """Create the config file."""
    today = date.today().isoformat()
    
    content = f"""filename = {html_filename}
title = {title}
description = 
keywords = 
created = {today}
updated = {today}
"""
    cfg_path.write_text(content, encoding='utf-8')

def convert_md_to_html(md_content: str, title: str) -> str:
    """Convert markdown content to HTML."""
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        md_content,
        extras=[
            "fenced-code-blocks",
            "tables",
            "header-ids",
            "metadata",
            "strike",
            "task_list"
        ]
    )
    
    # Create full HTML document
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
{html_content}
</body>
</html>"""
    
    return html_template

def process_markdown_file(md_path: str) -> None:
    """Process markdown file and generate cfg and html files."""
    md_path = Path(md_path)
    if not md_path.exists():
        print(f"Error: File not found: {md_path}")
        sys.exit(1)
    
    # Read markdown content
    md_content = md_path.read_text(encoding='utf-8')
    
    # Extract title
    title = extract_title_from_md(md_content)
    if not title:
        print("Error: No title (h1) found in markdown file")
        sys.exit(1)
    
    # Create pages directory if it doesn't exist
    pages_dir = Path("pages")
    next_num = get_next_number(pages_dir)
    
    # Generate filenames
    base_filename = sanitize_filename(md_path.stem)
    cfg_path = pages_dir / f"{next_num}-{base_filename}.cfg"
    html_path = pages_dir / f"{next_num}-{base_filename}.html"
    
    # Create cfg file
    create_cfg_file(cfg_path, f"{base_filename}.html", title)
    
    # Convert and save HTML
    html_content = convert_md_to_html(md_content, title)
    html_path.write_text(html_content, encoding='utf-8')
    
    print(f"Successfully created:")
    print(f"  Config file: {cfg_path}")
    print(f"  HTML file:  {html_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate cfg and html files from markdown file"
    )
    parser.add_argument(
        'markdown_file',
        help='Path to input markdown file'
    )
    
    args = parser.parse_args()
    process_markdown_file(args.markdown_file)

if __name__ == "__main__":
    main()
