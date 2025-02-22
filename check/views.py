from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Check, Printer
from .tasks import generatepdf

class Give_Check(APIView):
    def post(self, request):
        order = request.data.get('order', [])
        point_id = request.data.get('point_id')       

        printers = Printer.objects.filter(point_id=point_id)
        if not printers.exists():
            return Response({'message': 'No printers at this point'})
        
        existing_check = Check.objects.filter(order=order).first()


        for printer in printers:
            if not Check.objects.filter(order=order, printer=printer, type=printer.check_type).exists():
                check = Check.objects.create(
                    order=order,
                    printer=printer,
                    type=printer.check_type,
                    status='New',
                )
                check.save()
                generatepdf.delay(check.id)
            else:
                return Response({'message': 'A check for this order already exists for this printer.'})

        return Response({'message': 'Checks successfully created.'})
