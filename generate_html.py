#!/usr/bin/env python3
"""
HTML Generator for GreenAI Complete Guide
========================================

This script converts the comprehensive GreenAI guide to a beautiful HTML document
that can be easily printed to PDF or viewed in a browser.

Usage:
    python generate_html.py
"""

import os
import re
from datetime import datetime

def read_markdown_file():
    """Read the markdown file and return its content."""
    try:
        with open("GreenAI_Complete_Guide.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("❌ GreenAI_Complete_Guide.md not found")
        return None

def markdown_to_html(markdown_content):
    """Convert markdown to HTML with custom styling."""
    
    # Basic markdown to HTML conversion
    html = markdown_content
    
    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code class="\1">\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^(\d+)\. (.+)$', r'<li>\2</li>', html, flags=re.MULTILINE)
    
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Line breaks
    html = re.sub(r'\n\n', '</p><p>', html)
    html = re.sub(r'\n', '<br>', html)
    
    # Wrap in paragraphs
    html = '<p>' + html + '</p>'
    
    # Clean up empty paragraphs
    html = re.sub(r'<p></p>', '', html)
    html = re.sub(r'<p><br></p>', '', html)
    
    return html

def create_html_document(html_content):
    """Create a complete HTML document with styling."""
    
    css_style = """
    <style>
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'Inter', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }
        
        .header {
            background: linear-gradient(135deg, #228B22 0%, #98A869 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(34, 139, 34, 0.3);
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        h1 {
            color: #228B22;
            border-bottom: 3px solid #228B22;
            padding-bottom: 10px;
            margin-top: 40px;
            font-size: 2em;
        }
        
        h2 {
            color: #6B4F2A;
            margin-top: 30px;
            font-size: 1.5em;
            border-left: 4px solid #98A869;
            padding-left: 15px;
        }
        
        h3 {
            color: #98A869;
            margin-top: 25px;
            font-size: 1.3em;
        }
        
        h4 {
            color: #BE5103;
            margin-top: 20px;
            font-size: 1.1em;
        }
        
        p {
            margin: 15px 0;
            text-align: justify;
        }
        
        code {
            background-color: #f5f5f5;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
            font-size: 0.9em;
            color: #d63384;
        }
        
        pre {
            background-color: #f8f8f8;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #228B22;
            overflow-x: auto;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        pre code {
            background: none;
            padding: 0;
            color: #333;
        }
        
        ul, ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        
        li {
            margin: 8px 0;
        }
        
        blockquote {
            border-left: 4px solid #BE5103;
            margin: 20px 0;
            padding: 15px 20px;
            background-color: #f9f9f9;
            border-radius: 0 8px 8px 0;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 15px;
            text-align: left;
        }
        
        th {
            background-color: #98A869;
            color: white;
            font-weight: 600;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        .toc {
            background-color: #f5f5f5;
            padding: 25px;
            border-radius: 8px;
            margin: 30px 0;
            border-left: 4px solid #228B22;
        }
        
        .toc h2 {
            margin-top: 0;
            color: #228B22;
        }
        
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 8px 0;
            padding: 5px 0;
        }
        
        .toc a {
            color: #6B4F2A;
            text-decoration: none;
            font-weight: 500;
        }
        
        .toc a:hover {
            color: #228B22;
            text-decoration: underline;
        }
        
        .footer {
            background: linear-gradient(135deg, #6B4F2A 0%, #8B7355 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-top: 40px;
            text-align: center;
        }
        
        .footer p {
            margin: 5px 0;
        }
        
        .highlight {
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }
        
        .success {
            background-color: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
            margin: 15px 0;
        }
        
        .warning {
            background-color: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }
        
        .error {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
            margin: 15px 0;
        }
        
        @media print {
            body {
                background-color: white;
                color: black;
            }
            
            .header {
                background: #228B22 !important;
                -webkit-print-color-adjust: exact;
            }
            
            h1, h2, h3, h4 {
                color: #333 !important;
            }
            
            pre {
                border: 1px solid #ccc;
            }
        }
    </style>
    """
    
    html_document = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GreenAI Carbon Tracker - Complete Guide</title>
        {css_style}
    </head>
    <body>
        <div class="header">
            <h1>🌱 GreenAI Carbon Tracker</h1>
            <p>Complete Implementation Guide</p>
            <p>A Comprehensive Guide to Building Sustainable AI Development Tools</p>
        </div>
        
        {html_content}
        
        <div class="footer">
            <p><strong>🌿 GreenAI Carbon Tracker</strong></p>
            <p>Built with ❤️ for the environment • Making AI Development Sustainable</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
    </body>
    </html>
    """
    
    return html_document

def main():
    """Main function to generate HTML."""
    print("🌱 GreenAI HTML Generator")
    print("=" * 50)
    
    # Read markdown file
    markdown_content = read_markdown_file()
    if not markdown_content:
        return False
    
    print("📄 Converting markdown to HTML...")
    
    # Convert to HTML
    html_content = markdown_to_html(markdown_content)
    
    # Create complete HTML document
    html_document = create_html_document(html_content)
    
    # Write HTML file
    with open("GreenAI_Complete_Guide.html", "w", encoding="utf-8") as f:
        f.write(html_document)
    
    print("✅ HTML generated successfully!")
    print("📁 Output: GreenAI_Complete_Guide.html")
    print("\n💡 To convert to PDF:")
    print("   1. Open GreenAI_Complete_Guide.html in your browser")
    print("   2. Press Ctrl+P (or Cmd+P on Mac)")
    print("   3. Choose 'Save as PDF'")
    print("   4. Adjust settings and save")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 HTML generation completed successfully!")
        print("🌐 Open GreenAI_Complete_Guide.html in your browser to view")
    else:
        print("\n❌ HTML generation failed")
