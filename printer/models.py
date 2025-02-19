from django.db import models

class Printer(models.Model):
    name = models.CharField(max_length=120)
    object_location = models.CharField(max_length=120)