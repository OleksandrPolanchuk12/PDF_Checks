from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Check
from printer.models import Printer
from point.models import Point
from django.core.exceptions import ValidationError
from .tasks import generatepdf

class Give_Check(APIView):
    def post(self, request):
        order = request.data.get('order', [])
        point_id = request.data.get('point_id') 
        number_table = request.data.get('number_table')

        if not Point.objects.filter(id=point_id):
            return Response({'message': 'Point does not exist.'})      

        printers = Printer.objects.filter(point_id=point_id)
        if not printers.exists():
            return Response({'message': 'No printers at this point'})

        for printer in printers:
                try:
                    check = Check(
                        order=order,
                        printer=printer,
                        type=printer.check_type,
                        number_table=number_table,
                        status='new',
                    )
                    check.save()
                    generatepdf.delay(check.id)
                except ValidationError: 
                    return Response({'message': 'Check with this order already exists.'})
        return Response({'message': 'Checks successfully created.'})
