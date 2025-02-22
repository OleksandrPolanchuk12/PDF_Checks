from django.db import models
from printer.models import Printer
from django.core.exceptions import ValidationError


class Check(models.Model):

    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)  
    type = models.CharField(max_length=20, choices=[('kitchen', 'Kitchen'), ('client', 'Client')])  
    order = models.JSONField(default=dict)  
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('rendered', 'Rendered'), ('printed', 'Printed')])  
    pdf = models.FileField(upload_to='media/pdf/')  

    class Meta:
        unique_together = ('order', 'printer', 'type')

    @property
    def total_price(self):
        total = 0
        for item in self.order:
            price = item.get('price', 0)
            quantity = item.get('quantity', 1)
            total += price * quantity
        return total