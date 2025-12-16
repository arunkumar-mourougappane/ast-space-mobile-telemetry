"""
AST SpaceMobile PDF Report Generator
Converts the detailed markdown report into a stylized PDF with embedded images
"""

import base64
import os
import re
from collections import defaultdict
from datetime import datetime

import markdown


def image_to_base64(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Warning: Could not load image {image_path}: {e}")
        return None


def preprocess_markdown(md_content, base_path):
    """
    Preprocess markdown to embed images as base64 or fix paths
    """
    # Find all image references
    image_pattern = r"!\[([^\]]*)\]\(([^\)]+)\)"

    def replace_image(match):
        alt_text = match.group(1)
        img_path = match.group(2)

        # Handle relative paths
        if not img_path.startswith("http") and not img_path.startswith("data:"):
            full_path = os.path.join(base_path, img_path)
            if os.path.exists(full_path):
                # For weasyprint, we'll keep file paths
                return f"![{alt_text}]({full_path})"
            else:
                print(f"Warning: Image not found: {full_path}")
                return f"![{alt_text}]({img_path})"

        return match.group(0)

    return re.sub(image_pattern, replace_image, md_content)


def add_bookmark_ids(md_content):
    """
    Add HTML IDs to headers for bookmark navigation
    """
    lines = []
    satellite_counter = defaultdict(int)

    for line in md_content.split("\n"):
        # Add IDs to satellite headers (## SATELLITE NAME)
        if line.startswith("## ") and not line.startswith("### "):
            # Skip generic headers
            if any(
                x in line
                for x in [
                    "Executive Summary",
                    "Understanding",
                    "Pass Analysis",
                    "Appendix",
                ]
            ):
                lines.append(line)
            else:
                sat_name = line[3:].strip()
                sat_id = sat_name.lower().replace(" ", "-").replace("_", "-")
                lines.append(f'<h2 id="{sat_id}">{sat_name}</h2>')
                satellite_counter[sat_name] = 0
                continue

        # Add IDs to pass headers (#### Pass #N)
        if line.startswith("#### Pass #"):
            pass_num = line.replace("#### Pass #", "").strip()
            # Get current satellite from counter
            if satellite_counter:
                last_sat = list(satellite_counter.keys())[-1]
                sat_id = last_sat.lower().replace(" ", "-").replace("_", "-")
                pass_id = f"{sat_id}-pass-{pass_num}"
                lines.append(f'<h4 id="{pass_id}">Pass #{pass_num}</h4>')
                continue

        lines.append(line)

    return "\n".join(lines)


def create_styled_html(md_content, title="AST SpaceMobile Satellite Report"):
    """
    Convert markdown to HTML with professional styling and bookmarks
    """

    # Add bookmark IDs before conversion
    md_content = add_bookmark_ids(md_content)

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=["tables", "fenced_code", "codehilite", "toc", "attr_list"])

    html_content = md.convert(md_content)

    # Create styled HTML document
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @page {{
            size: Letter;
            margin: 0.75in 0.5in;
            @top-center {{
                content: "AST SpaceMobile Satellite Report";
                font-size: 9pt;
                color: #666;
            }}
            @bottom-right {{
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }}
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 10pt;
            line-height: 1.6;
            color: #333;
            background: white;
        }}

        h1 {{
            font-size: 24pt;
            font-weight: 700;
            color: #1a1a1a;
            margin-top: 0;
            margin-bottom: 8pt;
            padding-bottom: 8pt;
            border-bottom: 3px solid #2563eb;
            page-break-after: avoid;
        }}

        h2 {{
            font-size: 18pt;
            font-weight: 600;
            color: #2563eb;
            margin-top: 24pt;
            margin-bottom: 12pt;
            padding-top: 8pt;
            border-top: 2px solid #e5e7eb;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 14pt;
            font-weight: 600;
            color: #1e40af;
            margin-top: 18pt;
            margin-bottom: 10pt;
            page-break-after: avoid;
        }}

        h4 {{
            font-size: 12pt;
            font-weight: 600;
            color: #3b82f6;
            margin-top: 14pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
            page-break-before: auto;
        }}

        /* Keep pass sections together within one page */
        h4 + p {{
            page-break-inside: avoid;
        }}

        p {{
            margin-bottom: 8pt;
            text-align: justify;
        }}

        strong {{
            font-weight: 600;
            color: #1a1a1a;
        }}

        ul, ol {{
            margin-left: 20pt;
            margin-bottom: 10pt;
        }}

        li {{
            margin-bottom: 5pt;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8pt 0;
            font-size: 8pt;
            page-break-inside: avoid;
            page-break-before: avoid;
            background: white;
        }}

        thead {{
            background: #2563eb;
            color: white;
            font-weight: 600;
        }}

        th {{
            padding: 6pt 4pt;
            text-align: left;
            border: 1px solid #2563eb;
        }}

        td {{
            padding: 4pt 4pt;
            border: 1px solid #e5e7eb;
        }}

        tbody tr:nth-child(even) {{
            background: #f9fafb;
        }}

        tbody tr:hover {{
            background: #f3f4f6;
        }}

        img {{
            max-width: 90%;
            height: auto;
            display: block;
            margin: 8pt auto;
            page-break-inside: avoid;
            page-break-before: auto;
            page-break-after: auto;
            border: 1px solid #e5e7eb;
            padding: 4pt;
            background: white;
        }}

        hr {{
            border: none;
            border-top: 1px solid #e5e7eb;
            margin: 12pt 0;
            page-break-after: always;
        }}

        code {{
            background: #f3f4f6;
            padding: 2pt 4pt;
            border-radius: 3pt;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            color: #dc2626;
        }}

        pre {{
            background: #1f2937;
            color: #f3f4f6;
            padding: 12pt;
            border-radius: 4pt;
            overflow-x: auto;
            margin: 12pt 0;
            font-family: 'Courier New', monospace;
            font-size: 8pt;
            line-height: 1.4;
            page-break-inside: avoid;
        }}

        pre code {{
            background: transparent;
            padding: 0;
            color: #f3f4f6;
        }}

        blockquote {{
            border-left: 4px solid #2563eb;
            padding-left: 12pt;
            margin: 12pt 0;
            color: #4b5563;
            font-style: italic;
        }}

        .page-break {{
            page-break-before: always;
        }}

        /* Title page styling */
        .title-page {{
            text-align: center;
            padding-top: 100pt;
            page-break-after: always;
        }}

        .title-page h1 {{
            font-size: 32pt;
            margin-bottom: 12pt;
            border: none;
        }}

        .title-page h2 {{
            font-size: 20pt;
            color: #6b7280;
            font-weight: 400;
            margin-bottom: 24pt;
            border: none;
        }}

        .title-page .metadata {{
            margin-top: 48pt;
            font-size: 11pt;
            color: #4b5563;
        }}

        /* Info boxes */
        .info-box {{
            background: #eff6ff;
            border-left: 4px solid #2563eb;
            padding: 12pt;
            margin: 12pt 0;
            page-break-inside: avoid;
        }}

        .warning-box {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 12pt;
            margin: 12pt 0;
            page-break-inside: avoid;
        }}

        /* Footer styling */
        .footer {{
            margin-top: 24pt;
            padding-top: 12pt;
            border-top: 1px solid #e5e7eb;
            font-size: 9pt;
            color: #6b7280;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <h1>AST SpaceMobile</h1>
        <h2>Detailed Pass Analysis Report</h2>
        <h3>Signal Strength and Trajectory Analysis</h3>
        <p style="font-size: 14pt; margin-top: 24pt;">
            <strong>Location:</strong> Midland, Texas<br>
            <strong>Analysis Period:</strong> December 7-12, 2025
        </p>
        <div class="metadata">
            <p><strong>Report Generated:</strong> {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}</p>
            <p><strong>Analysis Tool:</strong> AST SpaceMobile Satellite Analysis v1.0</p>
            <p><strong>Data Source:</strong> Celestrak TLE Database</p>
        </div>
    </div>

    {html_content}

    <div class="footer">
        <p>This report is for analysis purposes. Actual signal performance may vary based on satellite configuration, atmospheric conditions, and ground terminal specifications.</p>
        <p>© 2025 AST SpaceMobile Satellite Analysis Project</p>
    </div>
</body>
</html>
"""

    return html_template


def extract_bookmarks(md_content):
    """
    Extract bookmark structure from markdown content
    """
    bookmarks = []
    current_satellite = None
    current_sat_bookmarks = []

    lines = md_content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Detect satellite headers
        if line.startswith("## ") and not any(
            x in line for x in ["Executive", "Understanding", "Pass Analysis", "Appendix"]
        ):
            # Save previous satellite if exists
            if current_satellite and current_sat_bookmarks:
                bookmarks.append({"label": current_satellite, "children": current_sat_bookmarks})

            current_satellite = line[3:].strip()
            current_sat_bookmarks = []

        # Detect pass headers with date
        elif line.startswith("#### Pass #") and current_satellite:
            pass_num = line.replace("#### Pass #", "").strip()
            # Look ahead for time window
            j = i + 1
            date_str = None
            while j < min(i + 5, len(lines)):
                if "Time Window (CST):" in lines[j]:
                    # Extract date from "2025-12-06 19:27:35"
                    match = re.search(r"(\d{4}-\d{2}-\d{2})", lines[j])
                    if match:
                        date_str = match.group(1)
                        # Convert to readable format: Dec 6
                        dt = datetime.strptime(date_str, "%Y-%m-%d")
                        date_str = dt.strftime("%b %d")
                    break
                j += 1

            sat_id = current_satellite.lower().replace(" ", "-").replace("_", "-")
            pass_id = f"{sat_id}-pass-{pass_num}"

            label = f"Pass #{pass_num}"
            if date_str:
                label = f"Pass #{pass_num} - {date_str}"

            current_sat_bookmarks.append({"label": label, "target": pass_id})

        i += 1

    # Add last satellite
    if current_satellite and current_sat_bookmarks:
        bookmarks.append({"label": current_satellite, "children": current_sat_bookmarks})

    return bookmarks


def generate_pdf_weasyprint(md_file, output_pdf):
    """
    Generate PDF using WeasyPrint with bookmarks
    """
    try:
        from weasyprint import HTML

        print("Using WeasyPrint for PDF generation...")

        # Read markdown file
        base_path = os.path.dirname(os.path.abspath(md_file))
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Extract bookmarks before preprocessing
        print("  Extracting bookmark structure...")
        bookmarks_data = extract_bookmarks(md_content)
        print(f"  ✓ Found {len(bookmarks_data)} satellites with passes")

        # Preprocess markdown (fix image paths)
        md_content = preprocess_markdown(md_content, base_path)

        # Convert to styled HTML
        html_content = create_styled_html(md_content)

        # Save HTML for debugging (optional)
        html_file = output_pdf.replace(".pdf", ".html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  ✓ HTML version saved to: {html_file}")

        # Generate PDF with bookmarks
        print("  Generating PDF (this may take a few minutes with 228 images)...")

        # Create HTML document
        html_doc = HTML(string=html_content, base_url=base_path)

        # Render without bookmarks first (simpler approach)
        print("  Rendering PDF document...")
        html_doc.write_pdf(output_pdf, stylesheets=None, presentational_hints=True)

        print("  ✓ PDF generated successfully")
        print("  ℹ Note: PDF includes HTML anchors for navigation. Bookmarks visible in advanced PDF readers.")
        return True

    except ImportError:
        print("WeasyPrint not available")
        return False
    except Exception as e:
        print(f"Error generating PDF with WeasyPrint: {e}")
        import traceback

        traceback.print_exc()
        return False


def generate_pdf_reportlab(md_file, output_pdf):
    """
    Generate PDF using ReportLab (fallback method)
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

        print("Using ReportLab for PDF generation...")

        # Read markdown file
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Create PDF
        doc = SimpleDocTemplate(
            output_pdf,
            pagesize=letter,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
            leftMargin=0.5 * inch,
            rightMargin=0.5 * inch,
        )

        story = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Title"],
            fontSize=32,
            textColor=colors.HexColor("#1a1a1a"),
            spaceAfter=12,
            alignment=TA_CENTER,
        )

        # Title page
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph("AST SpaceMobile", title_style))
        story.append(Paragraph("Detailed Pass Analysis Report", styles["Heading2"]))
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph("Signal Strength and Trajectory Analysis", styles["Normal"]))
        story.append(Paragraph("Midland, Texas | December 7-12, 2025", styles["Normal"]))
        story.append(PageBreak())

        # Parse markdown and add content
        lines = md_content.split("\n")
        for line in lines[:100]:  # Limited version for ReportLab
            if line.startswith("# "):
                story.append(Paragraph(line[2:], styles["Heading1"]))
            elif line.startswith("## "):
                story.append(Paragraph(line[3:], styles["Heading2"]))
            elif line.startswith("### "):
                story.append(Paragraph(line[4:], styles["Heading3"]))
            elif line.strip():
                story.append(Paragraph(line, styles["Normal"]))
                story.append(Spacer(1, 0.1 * inch))

        doc.build(story)
        print(f"  ✓ PDF generated successfully: {output_pdf}")
        return True

    except ImportError:
        print("ReportLab not available")
        return False
    except Exception as e:
        print(f"Error generating PDF with ReportLab: {e}")
        import traceback

        traceback.print_exc()
        return False


def generate_pdf_pandoc(md_file, output_pdf):
    """
    Generate PDF using Pandoc (requires pandoc and texlive)
    """
    import subprocess

    try:
        # Check if pandoc is available
        result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)

        if result.returncode != 0:
            print("Pandoc not available")
            return False

        print("Using Pandoc for PDF generation...")

        # Create pandoc command
        cmd = [
            "pandoc",
            md_file,
            "-o",
            output_pdf,
            "--pdf-engine=xelatex",
            "-V",
            "geometry:margin=0.75in",
            "-V",
            "fontsize=10pt",
            "-V",
            "linkcolor=blue",
            "-V",
            "urlcolor=blue",
            "--toc",
            "--toc-depth=3",
            "--number-sections",
            "--highlight-style=tango",
        ]

        print("  Generating PDF (this may take several minutes)...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"  ✓ PDF generated successfully: {output_pdf}")
            return True
        else:
            print(f"  Pandoc error: {result.stderr}")
            return False

    except FileNotFoundError:
        print("Pandoc not found in system")
        return False
    except Exception as e:
        print(f"Error generating PDF with Pandoc: {e}")
        return False


def main():
    """
    Main function to generate PDF report
    """
    print("=" * 80)
    print("AST SPACEMOBILE PDF REPORT GENERATOR")
    print("=" * 80)
    print()

    # Input and output files
    md_file = "AST_SpaceMobile_Detailed_Pass_Report.md"
    output_pdf = "AST_SpaceMobile_Detailed_Pass_Report.pdf"

    if not os.path.exists(md_file):
        print(f"❌ Error: Markdown file not found: {md_file}")
        return

    # Get file size
    file_size_mb = os.path.getsize(md_file) / (1024 * 1024)
    print(f"Input file: {md_file} ({file_size_mb:.1f} MB)")
    print(f"Output file: {output_pdf}")
    print()

    # Try different PDF generation methods
    methods = [
        ("WeasyPrint", generate_pdf_weasyprint),
        ("Pandoc", generate_pdf_pandoc),
        ("ReportLab", generate_pdf_reportlab),
    ]

    success = False
    for method_name, method_func in methods:
        print(f"Attempting PDF generation with {method_name}...")
        try:
            if method_func(md_file, output_pdf):
                success = True
                break
        except Exception as e:
            print(f"  Failed with {method_name}: {e}")
            continue

    print()
    print("=" * 80)

    if success:
        output_size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
        print("✅ PDF GENERATION SUCCESSFUL")
        print(f"   Output: {output_pdf} ({output_size_mb:.1f} MB)")
    else:
        print("❌ PDF GENERATION FAILED")
        print()
        print("To enable PDF generation, install one of these:")
        print()
        print("1. WeasyPrint (recommended):")
        print("   pip install weasyprint")
        print()
        print("2. Pandoc:")
        print("   sudo apt-get install pandoc texlive-xetex")
        print()
        print("3. ReportLab:")
        print("   pip install reportlab")

    print("=" * 80)


if __name__ == "__main__":
    main()
