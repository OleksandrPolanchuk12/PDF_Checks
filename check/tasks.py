import pdfkit
from celery import shared_task
from check.models import Check
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def generatepdf(id_check):
    check = Check.objects.get(id=id_check)
    file_name = f'{str(check.id).zfill(6)}_{check.type.lower()}.pdf'
    file_path = f'media/pdf/{file_name}' 

    html_file = f'{check.type.lower()}_check.html'

    context = {
        'check': check
    }
    html_string = render_to_string(html_file, context)
    options = {
        'enable-local-file-access': ''  
    }
    config = pdfkit.configuration()
    pdfkit.from_string(html_string, file_path, options=options)

    check.pdf.name = f'media/pdf/{file_name}'
    check.save()
