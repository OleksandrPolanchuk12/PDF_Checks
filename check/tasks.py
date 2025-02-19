from Issuing_checks.celery import app
from django.conf import settings
import subprocess
from django.core.files import File
from check.models import Check
import docker

@app.task
def Generate_PDF(id_order):
    check = Check.objects.get(id=id_order)
    file_name = f'{check.order.id_order}_{check.type_check.lower()}.pdf'
    file_path = f'media/pdf/{file_name}'

    html_file = f'templates/check/{check.type_check}_check.html'

    client = docker.from_env()

    container = client.containers.get()

    container.exec_run(f'wkhtmltopdf {html_file} {file_path}')

    check.pdf.save(file_name, File(open(file_path, 'rb')))
    
    check.save()