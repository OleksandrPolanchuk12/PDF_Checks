from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Check
from django.utils.timezone import now
from datetime import timedelta
from printer.models import Printer
from point.models import Point
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

        time = now() - timedelta(seconds=20)
        for printer in printers:
            if not Check.objects.filter(order=order, printer=printer, type=printer.check_type, created_at__gte=time).exists():
                check = Check.objects.create(
                    order=order,
                    printer=printer,
                    type=printer.check_type,
                    number_table=number_table,
                    status='new',
                )
                check.save()
                generatepdf.delay(check.id)
            else:
                return Response({'message': 'A check for this order already exists for this printer.'})

        return Response({'message': 'Checks successfully created.'})
