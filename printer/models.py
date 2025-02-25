from django.db import models

class Printer(models.Model):
    type=[('kitchen', 'Kitchen'), ('client', 'Client')]
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)
    check_type = models.CharField(max_length=20, choices=type)
    point_id = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.api_key:  
            last_printer = Printer.objects.order_by('-id').first()
            if last_printer:
                self.api_key = str(int(last_printer.api_key) + 1)  
            else:
                self.api_key = "1" 
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name