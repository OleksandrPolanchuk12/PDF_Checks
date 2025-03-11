from django.shortcuts import render
from printer.models import Printer
from rest_framework.views import APIView
from check.models import Check
from .serializers import CheckSerializers   
from rest_framework.response import Response
from point.models import Point


class GetCheckView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key' , None)
        printer = Printer.objects.get(api_key=api_key)
        checks = Check.objects.filter(printer=printer)
        if checks.exists():
            serializers = CheckSerializers(checks, many=True)
            return Response({'checks': f'{serializers.data}'})
        else:
            return Response({'message': 'No checks for this printer'})
        

class PrintChecksView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key', None)

        printer = Printer.objects.get(api_key=api_key)
        if not printer.exists():
            return Response({'message': 'No printer found with this API key'})
        
        checks = Check.objects.filter(printer=printer, status='New')
        if not checks.exists():
            return Response({'message': 'No new checks for this printer'})
        if checks.exists():
            for check in checks:
                # відправка pdf чеку на принтер.
                check.status = 'rendered'
                check.save()


class AddPrinterView(APIView):
    def post(self, request):
        name = request.data.get('name', None)
        check_type = request.data.get('check_type', None)
        point_id = request.data.get('point_id', None)

        if not Point.objects.filter(id=point_id):
            return Response({'message': 'Point does not exist.'})  
            
        if not name or not check_type or not point_id:
            return Response({'message': 'All fields are required'})
        printer = Printer.objects.create(name=name,check_type = check_type, point_id = point_id)
        printer.save()
        return Response({'message': 'Printer added'})


class EditPrinterView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key', None)
        new_name = request.data.get('new_name', self.name)
        new_type = request.data.get('new_check_type', self.check_type)
        new_point_id = request.data.get('new_point_id', self.point_id)

        printer = Printer.objects.get(api_key=api_key)
        if new_name:
                printer.name = new_name
        if new_type:
            printer.check_type = new_type
        if new_point_id:
            printer.point_id = new_point_id

        printer.save()
        return Response({'message': 'Printer edited'})


class DeletePrinterView(APIView):
    def post(self, request):
        api_key = request.data.get('api_key', None)

        if not api_key:
            return Response({'message': 'API Key is required'})
        try:
            printer = Printer.objects.get(api_key=api_key)
            printer.delete()
            return Response({'message': 'Printer deleted successfully'})
        except Printer.DoesNotExist:
            return Response({'message': 'Printer not found'})
    