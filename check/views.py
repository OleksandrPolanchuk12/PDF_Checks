from django.shortcuts import render
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework import serializers
from printer.models import Printer
from check.models import Check
from rest_framework.response import Response
from .tasks import generatepdf


class Give_Check(APIView):
    def post(self, request):
        order = request.data.get('order', [])
        point_id = request.data.get('point_id')       
        
        printers = Printer.objects.filter(point_id=point_id)
        if not printers.exists():
            return Response({'No printers at this point'})
    

        for printer in printers:        
            if not Check.objects.filter(order=order, printer=printer, type=printer.check_type).exists():
                check = Check.objects.create(order=order, printer=printer, type=printer.check_type)
                generatepdf.delay(check.id)
            else:
                return Response({'message': 'A check for this order already exists.'})

        
        return Response({'message':'Checks successfully created'})


