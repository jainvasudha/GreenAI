#!/usr/bin/env python3
"""
GreenAI PDF Creation Guide
=========================

This script provides multiple methods to create a PDF from the GreenAI Complete Guide.

Methods:
1. HTML to PDF (Browser print)
2. Markdown to PDF (Pandoc)
3. Python libraries (ReportLab, WeasyPrint)
4. Online converters

Usage:
    python create_pdf_guide.py
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists():
    """Check if the required files exist."""
    files_to_check = [
        "GreenAI_Complete_Guide.md",
        "GreenAI_Complete_Guide.html"
    ]
    
    missing_files = []
    for file in files_to_check:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def method_1_browser_print():
    """Method 1: Use browser print to PDF."""
    print("\n🌐 Method 1: Browser Print to PDF")
    print("-" * 40)
    print("1. Open GreenAI_Complete_Guide.html in your browser")
    print("2. Press Ctrl+P (Windows/Linux) or Cmd+P (Mac)")
    print("3. In the print dialog:")
    print("   - Destination: Save as PDF")
    print("   - Layout: Portrait")
    print("   - Paper size: A4")
    print("   - Margins: Default")
    print("4. Click 'Save' and choose filename: GreenAI_Complete_Guide.pdf")
    print("\n✅ This method produces the best quality PDF with proper formatting")

def method_2_pandoc():
    """Method 2: Use Pandoc to convert markdown to PDF."""
    print("\n📚 Method 2: Pandoc Conversion")
    print("-" * 40)
    
    # Check if pandoc is available
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
        print("✅ Pandoc is available")
        
        print("\n🔄 Converting with pandoc...")
        cmd = [
            "pandoc",
            "GreenAI_Complete_Guide.md",
            "-o", "GreenAI_Complete_Guide.pdf",
            "--pdf-engine=wkhtmltopdf",
            "--metadata", "title=GreenAI Carbon Tracker - Complete Guide",
            "--metadata", "author=GreenAI Team",
            "--metadata", "date=2024-10-24",
            "--toc",
            "--toc-depth=3"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PDF generated successfully with pandoc")
            return True
        else:
            print(f"❌ Pandoc conversion failed: {result.stderr}")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Pandoc not available")
        print("💡 Install pandoc:")
        print("   - macOS: brew install pandoc")
        print("   - Ubuntu: sudo apt install pandoc")
        print("   - Windows: Download from https://pandoc.org/installing.html")
        return False

def method_3_python_libraries():
    """Method 3: Use Python libraries to create PDF."""
    print("\n🐍 Method 3: Python Libraries")
    print("-" * 40)
    
    # Try WeasyPrint
    try:
        import weasyprint
        import markdown2
        
        print("✅ WeasyPrint available, generating PDF...")
        
        # Read HTML file
        with open("GreenAI_Complete_Guide.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Convert to PDF
        weasyprint.HTML(string=html_content).write_pdf("GreenAI_Complete_Guide.pdf")
        print("✅ PDF generated successfully with WeasyPrint")
        return True
        
    except ImportError:
        print("⚠️  WeasyPrint not available")
        print("💡 Install with: pip install weasyprint")
        
        # Try ReportLab as fallback
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            
            print("✅ ReportLab available, generating simple PDF...")
            
            # Create simple PDF
            doc = SimpleDocTemplate("GreenAI_Complete_Guide.pdf", pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Read markdown and convert to simple PDF
            with open("GreenAI_Complete_Guide.md", "r", encoding="utf-8") as f:
                content = f.read()
            
            story = []
            lines = content.split('\n')
            
            for line in lines:
                if line.startswith('# '):
                    story.append(Paragraph(line[2:], styles['Heading1']))
                    story.append(Spacer(1, 12))
                elif line.startswith('## '):
                    story.append(Paragraph(line[3:], styles['Heading2']))
                    story.append(Spacer(1, 6))
                elif line.strip():
                    story.append(Paragraph(line, styles['Normal']))
                    story.append(Spacer(1, 3))
            
            doc.build(story)
            print("✅ Simple PDF generated with ReportLab")
            return True
            
        except ImportError:
            print("⚠️  ReportLab not available")
            print("💡 Install with: pip install reportlab")
            return False

def method_4_online_converters():
    """Method 4: Use online converters."""
    print("\n🌐 Method 4: Online Converters")
    print("-" * 40)
    print("1. Upload GreenAI_Complete_Guide.html to an online converter:")
    print("   - https://www.ilovepdf.com/html_to_pdf")
    print("   - https://www.sodapdf.com/html-to-pdf/")
    print("   - https://www.freepdfconvert.com/html-to-pdf")
    print("2. Download the converted PDF")
    print("\n✅ This method works without installing additional software")

def method_5_system_tools():
    """Method 5: Use system tools."""
    print("\n🖥️  Method 5: System Tools")
    print("-" * 40)
    
    # Check for wkhtmltopdf
    try:
        subprocess.run(["wkhtmltopdf", "--version"], capture_output=True, check=True)
        print("✅ wkhtmltopdf available")
        
        print("🔄 Converting HTML to PDF...")
        cmd = [
            "wkhtmltopdf",
            "--page-size", "A4",
            "--margin-top", "20mm",
            "--margin-bottom", "20mm",
            "--margin-left", "20mm",
            "--margin-right", "20mm",
            "GreenAI_Complete_Guide.html",
            "GreenAI_Complete_Guide.pdf"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PDF generated successfully with wkhtmltopdf")
            return True
        else:
            print(f"❌ wkhtmltopdf conversion failed: {result.stderr}")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  wkhtmltopdf not available")
        print("💡 Install wkhtmltopdf:")
        print("   - macOS: brew install wkhtmltopdf")
        print("   - Ubuntu: sudo apt install wkhtmltopdf")
        print("   - Windows: Download from https://wkhtmltopdf.org/downloads.html")
        return False

def main():
    """Main function to provide PDF creation options."""
    print("🌱 GreenAI PDF Creation Guide")
    print("=" * 50)
    
    # Check if required files exist
    if not check_file_exists():
        return False
    
    print("\n📋 Available PDF Creation Methods:")
    print("=" * 50)
    
    # Method 1: Browser print (always available)
    method_1_browser_print()
    
    # Method 2: Pandoc
    method_2_pandoc()
    
    # Method 3: Python libraries
    method_3_python_libraries()
    
    # Method 4: Online converters
    method_4_online_converters()
    
    # Method 5: System tools
    method_5_system_tools()
    
    print("\n🎯 Recommended Approach:")
    print("=" * 50)
    print("1. 🥇 BEST: Use Method 1 (Browser Print) for highest quality")
    print("2. 🥈 GOOD: Use Method 2 (Pandoc) if you have pandoc installed")
    print("3. 🥉 OKAY: Use Method 3 (Python libraries) for automated generation")
    
    print("\n📁 Output Files:")
    print("=" * 50)
    if os.path.exists("GreenAI_Complete_Guide.pdf"):
        print("✅ GreenAI_Complete_Guide.pdf (Generated)")
    else:
        print("⚠️  GreenAI_Complete_Guide.pdf (Not generated yet)")
    
    print("✅ GreenAI_Complete_Guide.html (Available for browser print)")
    print("✅ GreenAI_Complete_Guide.md (Source markdown)")
    
    print("\n🌿 Happy PDF creation!")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 PDF creation guide completed!")
        print("📖 Choose your preferred method and create your PDF")
    else:
        print("\n❌ PDF creation guide failed")
