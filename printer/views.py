from django.shortcuts import render, get_object_or_404
from printer.models import Printer
from rest_framework.views import APIView
from check.models import Check
from .serializers import CheckSerializers   
from rest_framework.response import Response
from point.models import Point

class GetCheckView(APIView):
    def post(self, request):

        printer_id = request.data.get('id', None)
        printer = get_object_or_404(Printer, id=printer_id)
        checks = Check.objects.filter(printer=printer)
        if checks.exists():
            serializers = CheckSerializers(checks, many=True)
            return Response({'checks': f'{serializers.data}'})
        else:
            return Response({'message': 'No checks for this printer'})
        

class PrintChecksView(APIView):
    def post(self, request):
        id = request.data.get('id', None)

        printer = Printer.objects.get(id=id)
        if not printer.exists():
            return Response({'message': 'No printer found with this id'})
        
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

        if not name or not check_type or not point_id:
            return Response({'message': 'All fields are required'})

        point = get_object_or_404(Point, id=point_id)

        if check_type not in ['client', 'kitchen']:
            return Response({'message': f'There is no such thing as a {str(check_type)} printer.'})
        
        if Printer.objects.filter(check_type=check_type, point_id=point).exists():
            return Response({'message': 'Printer already exists'})
        
        api_key_obj = request.auth
        printer = Printer.objects.create(name=name,check_type = check_type, point_id = point, api_key=api_key_obj)
        printer.save()
        return Response({'message': 'Printer added'})


class EditPrinterView(APIView):

    def post(self, request):
        id_printer = request.data.get('id', None)
        new_name = request.data.get('new_name')
        new_type = request.data.get('new_check_type')
        new_point_id = request.data.get('new_point_id')

        point = get_object_or_404(Point, id=new_point_id)
        
        printer = get_object_or_404(Printer, id=id_printer)
        if new_name:
            printer.name = new_name
        if new_type:
            printer.check_type = new_type
        if new_point_id:
            printer.point_id = point

        printer.save()
        return Response({'message': 'Printer edited'})


class DeletePrinterView(APIView):
    def post(self, request):
        id_printer = request.data.get('id', None)

        if not id_printer:
            return Response({'message': 'Id is required'})
        try:
            printer = Printer.objects.get(id=id_printer)
            printer.delete()
            return Response({'message': 'Printer deleted successfully'})
        except Printer.DoesNotExist:
            return Response({'message': 'Printer not found'})
    