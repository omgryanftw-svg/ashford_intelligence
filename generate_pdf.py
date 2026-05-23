from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

FONT_SEARCH_PATHS = [
    '/Library/Fonts',
    '/System/Library/Fonts',
    os.path.expanduser('~/Library/Fonts'),
    os.path.join(os.getcwd(), 'assets', 'fonts'),
]

FONT_CANDIDATES = [
    ('SF Pro Display', ['SF-Pro-Display-Regular.ttf', 'SFProDisplay-Regular.otf', 'SFProDisplay-Regular.ttf']),
    ('SF Pro Text', ['SF-Pro-Text-Regular.ttf', 'SFProText-Regular.otf', 'SFProText-Regular.ttf']),
    ('Inter', ['Inter-Regular.ttf', 'Inter-Regular.otf']),
    ('DejaVuSans', ['DejaVuSans.ttf', 'DejaVuSans.otf']),
]


def find_font_file(names):
    for base in FONT_SEARCH_PATHS:
        if not os.path.isdir(base):
            continue
        for root, _, files in os.walk(base):
            for candidate in names:
                if candidate in files:
                    return os.path.join(root, candidate)
    return None

body_font = 'Times-Roman'
for family, names in FONT_CANDIDATES:
    found = find_font_file(names)
    if found:
        try:
            pdfmetrics.registerFont(TTFont(family, found))
            body_font = family
            break
        except Exception:
            continue

doc = SimpleDocTemplate("privacy-policy.pdf", pagesize=A4, rightMargin=36,leftMargin=36,topMargin=54,bottomMargin=54)
styles = getSampleStyleSheet()
normal = ParagraphStyle('NormalCustom', parent=styles['Normal'], fontName=body_font, fontSize=11, leading=14, spaceAfter=8)
title_style = ParagraphStyle('Title', parent=styles['Title'], fontName=body_font, fontSize=18, leading=22, spaceAfter=14, alignment=0)
heading = ParagraphStyle('Heading', parent=styles['Heading2'], fontName=body_font, fontSize=13, leading=16, spaceBefore=8, spaceAfter=6)

flow = []
with open('privacy-policy.txt','r') as f:
    txt = f.read()

flow.append(Paragraph('ASHFORD INTELLIGENCE — PRIVACY POLICY', title_style))
flow.append(Spacer(1,6))

for block in txt.split('\n\n'):
    block = block.strip()
    if not block:
        continue
    firstline = block.split('\n',1)[0]
    # Treat short lines in ALL CAPS or lines ending with ':' as headings
    if (firstline.isupper() and len(firstline) < 60) or (firstline.strip().endswith(':') and '\n' not in block):
        flow.append(Paragraph(firstline.replace('\n','<br/>'), heading))
        rest = block[len(firstline):].strip()
        if rest:
            flow.append(Paragraph(rest.replace('\n','<br/>'), normal))
    else:
        flow.append(Paragraph(block.replace('\n','<br/>'), normal))
    flow.append(Spacer(1,6))

generated_on = datetime.utcnow().strftime('%Y-%m-%d UTC')

def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFont(body_font, 9)
    canvas.setFillColorRGB(0.2,0.2,0.2)
    # Header
    canvas.drawCentredString(width/2.0, height - 30, 'Ashford Intelligence — Privacy Policy')
    # Footer: page number and generation date
    canvas.setFont(body_font, 9)
    canvas.drawString(36, 30, f'Generated: {generated_on}')
    canvas.drawRightString(width - 36, 30, f'Page {doc.page}')
    canvas.restoreState()

doc.build(flow, onFirstPage=header_footer, onLaterPages=header_footer)
print('PDF generated: privacy-policy.pdf')
