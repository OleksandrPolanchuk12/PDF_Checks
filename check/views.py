from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers
from printer.models import Printer
from check.models import Check
from order.models import Order
from django.http import JsonResponse
from .tasks import Generate_PDF


class Give_Check(APIView):
    def post(self, request):
        data = request.data.get('data', [])
        object_location = request.data.get('object_location')       
        
        printers = Printer.objects.all(object_location=object_location)
        if not printers.exists():
            return JsonResponse({'Принтерів на цій точці немає'})
        
        order = Order.objects.create(data=data)

        for printer in printers:
            for type in ['client', 'kitchen']:
                check = Check.objects.create(order=order, printer=printer, type=type)
                Generate_PDF.delay(check.id)
        
        return JsonResponse({'message':'Чеки успішно створені'})


