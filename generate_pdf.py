#!/usr/bin/env python3
"""
PDF Generator for GreenAI Complete Guide
=======================================

This script converts the comprehensive GreenAI guide to a professional PDF document.

Requirements:
- markdown2
- weasyprint (for PDF generation)
- Or use pandoc (if available)

Usage:
    python generate_pdf.py
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required packages for PDF generation."""
    try:
        import markdown2
        import weasyprint
        print("✅ Required packages already installed")
        return True
    except ImportError:
        print("📦 Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown2", "weasyprint"])
            print("✅ Packages installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            return False

def convert_with_pandoc():
    """Convert markdown to PDF using pandoc."""
    try:
        # Check if pandoc is available
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        
        print("🔄 Converting with pandoc...")
        cmd = [
            "pandoc",
            "GreenAI_Complete_Guide.md",
            "-o", "GreenAI_Complete_Guide.pdf",
            "--pdf-engine=wkhtmltopdf",
            "--css=style.css",
            "--metadata", "title=GreenAI Carbon Tracker - Complete Guide",
            "--metadata", "author=GreenAI Team",
            "--metadata", "date=2024-10-24"
        ]
        
        subprocess.run(cmd, check=True)
        print("✅ PDF generated successfully with pandoc")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Pandoc not available, trying alternative method...")
        return False

def convert_with_weasyprint():
    """Convert markdown to PDF using weasyprint."""
    try:
        import markdown2
        import weasyprint
        
        print("🔄 Converting with weasyprint...")
        
        # Read markdown file
        with open("GreenAI_Complete_Guide.md", "r", encoding="utf-8") as f:
            markdown_content = f.read()
        
        # Convert to HTML
        html_content = markdown2.markdown(
            markdown_content,
            extras=[
                'fenced-code-blocks',
                'tables',
                'header-ids',
                'toc'
            ]
        )
        
        # Add CSS styling
        css_content = """
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'Inter', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        h1 {
            color: #228B22;
            border-bottom: 3px solid #228B22;
            padding-bottom: 10px;
        }
        
        h2 {
            color: #6B4F2A;
            margin-top: 30px;
        }
        
        h3 {
            color: #98A869;
        }
        
        code {
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Monaco', 'Consolas', monospace;
        }
        
        pre {
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #228B22;
            overflow-x: auto;
        }
        
        blockquote {
            border-left: 4px solid #BE5103;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #f9f9f9;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: #98A869;
            color: white;
        }
        
        .toc {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        """
        
        # Create full HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>GreenAI Carbon Tracker - Complete Guide</title>
            <style>{css_content}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Convert to PDF
        weasyprint.HTML(string=full_html).write_pdf("GreenAI_Complete_Guide.pdf")
        print("✅ PDF generated successfully with weasyprint")
        return True
        
    except Exception as e:
        print(f"❌ Failed to generate PDF with weasyprint: {e}")
        return False

def create_simple_pdf():
    """Create a simple text-based PDF as fallback."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        print("🔄 Creating simple PDF with reportlab...")
        
        # Read markdown file
        with open("GreenAI_Complete_Guide.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Create PDF
        doc = SimpleDocTemplate("GreenAI_Complete_Guide.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            textColor='#228B22'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor='#6B4F2A'
        )
        
        # Parse content
        story = []
        lines = content.split('\n')
        
        for line in lines:
            if line.startswith('# '):
                story.append(Paragraph(line[2:], title_style))
                story.append(Spacer(1, 12))
            elif line.startswith('## '):
                story.append(Paragraph(line[3:], heading_style))
                story.append(Spacer(1, 6))
            elif line.startswith('### '):
                story.append(Paragraph(line[4:], styles['Heading3']))
                story.append(Spacer(1, 3))
            elif line.strip():
                story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 3))
        
        doc.build(story)
        print("✅ Simple PDF generated successfully")
        return True
        
    except ImportError:
        print("❌ ReportLab not available")
        return False
    except Exception as e:
        print(f"❌ Failed to generate simple PDF: {e}")
        return False

def main():
    """Main function to generate PDF."""
    print("🌱 GreenAI PDF Generator")
    print("=" * 50)
    
    # Check if markdown file exists
    if not os.path.exists("GreenAI_Complete_Guide.md"):
        print("❌ GreenAI_Complete_Guide.md not found")
        return False
    
    print("📄 Found GreenAI_Complete_Guide.md")
    
    # Try different conversion methods
    methods = [
        ("Pandoc", convert_with_pandoc),
        ("WeasyPrint", convert_with_weasyprint),
        ("ReportLab", create_simple_pdf)
    ]
    
    for method_name, method_func in methods:
        print(f"\n🔄 Trying {method_name}...")
        if method_name == "WeasyPrint":
            if not install_requirements():
                continue
        
        if method_func():
            print(f"\n🎉 PDF generated successfully using {method_name}!")
            print("📁 Output: GreenAI_Complete_Guide.pdf")
            return True
    
    print("\n❌ All conversion methods failed")
    print("💡 Try installing pandoc: brew install pandoc (macOS) or apt install pandoc (Ubuntu)")
    return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🌿 PDF generation completed successfully!")
        print("📖 You can now share the GreenAI Complete Guide PDF")
    else:
        print("\n⚠️  PDF generation failed, but the markdown guide is still available")
        print("📄 Read GreenAI_Complete_Guide.md directly")
