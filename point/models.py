from django.db import models

class Point(models.Model):
    address = models.CharField(max_length=255)
