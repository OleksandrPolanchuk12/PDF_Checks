from django.db import models
from printer.models import Printer
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ValidationError

class Check(models.Model):

    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)  
    type = models.CharField(max_length=20, choices=[('kitchen', 'Kitchen'), ('client', 'Client')])  
    order = models.JSONField(default=dict)  
    status = models.CharField(max_length=20, choices=[('new', 'New'), ('rendered', 'Rendered'), ('printed', 'Printed')])  
    number_table = models.CharField(null=False, blank=True)
    pdf = models.FileField(upload_to='media/pdf/')  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Чек {self.id}"
    
    def save(self, *args, **kwargs):
        time = now() - timedelta(seconds=20)
        try:
            check = Check.objects.get(order=self.order, printer=self.printer, type=self.type, created_at__gte=time)
        except Check.DoesNotExist:
            raise ValidationError('Check with this order already exists')
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        total = 0
        for item in self.order:
            price = item.get('price', 0)
            quantity = item.get('quantity', 1)
            total += price * quantity
        return total
    