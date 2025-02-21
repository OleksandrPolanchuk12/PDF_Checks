from django.contrib import admin
from .models import Printer

@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'point_id')

    def point_id(self, obj):
        return obj.point_id