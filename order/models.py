from django.db import models

class Order(models.Model):
    id_order = models.CharField(max_length=6, unique=True, null=True)
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_date_now = True)

    def save(self, *args, **kwargs):
        if not self.id_order:
            last_order = Order.objects.order_by('-id_order').first()
            if last_order:
                new_id = str(int(last_order.id_order) + 1).zfill(6) 
            else:
                new_id = '000001' 
            self.id_order = new_id
        super().save(*args, **kwargs)