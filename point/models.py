from django.db import models

class Point(models.Model):
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Точка  {self.id} "
