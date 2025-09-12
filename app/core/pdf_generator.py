import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.apis.transactions.models import Transaction

try:
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
    FONT_NAME = "DejaVuSans"
    FONT_NAME_BOLD = "DejaVuSans-Bold"
except Exception as e:
    FONT_NAME = "Helvetica"
    FONT_NAME_BOLD = "Helvetica-Bold"


def create_receipt_pdf_with_reportlab(transaction: Transaction) -> bytes:
    """
    Генерує PDF-квитанцію за допомогою reportlab і повертає її як байти.
    """
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4 
    
    p.setFont(FONT_NAME_BOLD, 20)
    p.drawCentredString(width / 2.0, height - 2*cm, f"Receipt:{transaction.id}")

    p.line(2*cm, height - 2.5*cm, width - 2*cm, height - 2.5*cm)

    p.setFont(FONT_NAME, 12)
    text = p.beginText(2*cm, height - 3.5*cm)
    text.setLeading(18) 

    sender_email = transaction.sender_account.user.email
    recipient_email = transaction.recipient_account.user.email
    

    text.textLine(f"Date & Time: {transaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    text.textLine(f"Sender: {sender_email}") 
    text.textLine(f"Recipient: {recipient_email}") 
    text.textLine(f"Description: {transaction.description or 'Not specified'}")
    
    p.drawText(text)

    p.setFont(FONT_NAME_BOLD, 16)
    amount_str = f'Total Amount: {"%.2f" % transaction.amount} USD'
    p.drawRightString(width - 2*cm, height - 8*cm, amount_str)
    
    p.showPage()
    p.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes