from django.shortcuts import render
from printer.models import Printer
from rest_framework.views import APIView
from check.models import Check
from rest_framework import serializers
from rest_framework.response import Response


class GetCheckView(APIView):
    def get(self, request, id_printer):
        printer = Printer.objects.get(id=id_printer)
        checks = Check.objects.filter(printer=printer, status='new')
        if checks.exists():
            serializers = CheckSerializers(checks, many=True)
            return Response(serializers.data, safe=False)
        else:
            return Response({'message': 'Немає чеків для даного принтера'})

    
class CheckSerializers(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = ('id', 'pdf', 'status')
