from django.contrib import admin
from .models import Check

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_display = ('order', 'printer', 'type', 'status','created_at')
    list_filter = ('type', 'status', 'printer','created_at')
