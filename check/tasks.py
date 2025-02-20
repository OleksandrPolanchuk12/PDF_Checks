from Issuing_checks.celery import app
from django.template.loader import render_to_string
from django.conf import settings
import subprocess
from django.core.files import File
from check.models import Check
import docker

@app.task
def Generate_PDF(id_check):
    check = Check.objects.get(id=id_check)
    file_name = f'{str(check.id).zfill(6)}_{check.type.lower()}.pdf'
    file_path = f'media/pdf/{file_name}'

    html_file = f'templates/check/{check.type}_check.html'

    context = {
        'check': check,
    }
    content = render_to_string(html_file, context)

    client = docker.from_env()

    container = client.containers.get('cfcaf30981a2')

    with open(file_path, 'w') as f:
        container.exec_run(f'wkhtmltopdf - -', stdin=content.encode(), stdout=f)

    check.pdf.save(file_name, File(open(file_path, 'rb')))
    
    check.save()