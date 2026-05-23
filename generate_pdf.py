from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

# Register a common fallback font (DejaVu if available, else Times-Roman will be used)
try:
    pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    body_font = 'DejaVuSans'
except Exception:
    body_font = 'Times-Roman'

doc = SimpleDocTemplate("privacy-policy.pdf", pagesize=A4, rightMargin=36,leftMargin=36,topMargin=54,bottomMargin=54)
styles = getSampleStyleSheet()
normal = ParagraphStyle('NormalCustom', parent=styles['Normal'], fontName=body_font, fontSize=11, leading=14, spaceAfter=8)
title_style = ParagraphStyle('Title', parent=styles['Title'], fontName=body_font, fontSize=16, leading=20, spaceAfter=12, alignment=0)
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
