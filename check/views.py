from django.shortcuts import render
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework import serializers
from printer.models import Printer
from check.models import Check
from rest_framework.response import Response
from .tasks import Generate_PDF


class Give_Check(APIView):
    def post(self, request):
        order = request.data.get('order', [])
        point_id = request.data.get('point_id')       
        
        printers = Printer.objects.filter(point_id=point_id)
        if not printers.exists():
            return Response({'Принтерів на цій точці немає'})
    

        for printer in printers:
            for type in ['client', 'kitchen']:
                check = Check.objects.create(order=order, printer=printer, type=type)
                Generate_PDF.delay(check.id)
        
        return Response({'message':'Чеки успішно створені'})


