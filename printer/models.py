from django.db import models

class Printer(models.Model):
    type=[('kitchen', 'Kitchen'), ('client', 'Client')]
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)
    check_type = models.CharField(max_length=20, choices=type)
    point_id = models.IntegerField()

    def __str__(self):
        return self.name