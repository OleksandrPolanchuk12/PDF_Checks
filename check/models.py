from django.db import models
from order.models import Order
from printer.models import Printer
from django.core.exceptions import ValidationError


class Check(models.Model):
    type_check = [('client','Client'),('kitchen','Kitchen')]
    status_check = [('Pending','pending'),('printed','Printed')]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=type_check)
    status = models.CharField(max_length=7, choices=status_check, default='pending')
    pdf = models.FileField(upload_to='media/pdf/', null=True, blank=True)

    class Meta:
        unique_together = ('order', 'printer', 'type')

    def save(self, *args, **kwargs):
        if Check.objects.filter(order=self.order, printer=self.printer, type=self.type).exists():
            raise ValidationError(f"Чек для замовлення {self.order.id_order} на принтері {self.printer.name} для {self.type} вже існує.")

        super().save(*args, **kwargs)