from django.shortcuts import render
from printer.models import Printer
from rest_framework.views import APIView
from check.models import Check
from rest_framework import serializers
from django.http import JsonResponse


class GetCheckView(APIView):
    def get(self, request, id_printer):
        printer = Printer.objects.get(id=id_printer)
        checks = Check.objects.filter(printer=printer, status='pending')
        if checks.exists():
            serializers = CheckSerializers(checks, many=True)
            return JsonResponse(serializers.data, safe=False)
        else:
            return JsonResponse({'message': 'Немає чеків для даного принтера'})

    
class CheckSerializers(serializers.ModelSerializers):
    class Meta:
        model = Check
        fields = ('id', 'pdf')
