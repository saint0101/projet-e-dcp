"""
Fonction pour la génération des fichiers PDF.
"""

from datetime import datetime
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.contrib import messages
from django.urls import reverse
# from weasyprint import HTML
from xhtml2pdf import pisa
from io import BytesIO
import qrcode
from PIL import Image


PDF_TEMPLATES = {
  # Lettre d'approbation du Correspondant
  'correspondant_approbation': 'pdfs/correspondant/approbation_client.html'
}

def generate_pdf(request, template, context):
  """ Fonction de génération de PDF
  Paramètres :
  context - doit contenir pk et url_path
  """
  qr_code = generate_qrcode(request, context)
  context['qr_code'] = qr_code
  context['date'] = datetime.now().strftime('%d/%m/%Y')

  html = render_to_string(template, context)
  # print('html', html)
  # pdf = HTML(string=html).write_pdf()
  pdf = BytesIO()
  pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf)
  pdf.seek(0) # remise à zero du pointeur (au début du fichier)

  if pisa_status.err:
    messages.error(request, 'Le PDF n\'a pas pus être généré')
    print('Le PDF n\'a pas pus être généré', pisa_status.err)
    return None
  
  return ContentFile(pdf.read())
  # return html
  

def generate_qrcode(request, context):
  print('context', context)
  # url = request.build_absolute_uri(reverse(context['url_path'], args=context['pk']))
  url = request.build_absolute_uri(reverse(context['url_path'], args=[context['pk'],]))
  # print('url', url)
  qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
  )
  qr.add_data(url)
  qr.make(fit=True)
  img = qr.make_image(fill="black", back_color="white")

  # Convert PIL image to byte array
  img_bytes = BytesIO()
  img.save(img_bytes, format='PNG')
  img_bytes = img_bytes.getvalue()

  # Encode the QR code image as base64 to embed it in HTML
  import base64
  qr_code_base64 = base64.b64encode(img_bytes).decode('utf-8')

  return qr_code_base64