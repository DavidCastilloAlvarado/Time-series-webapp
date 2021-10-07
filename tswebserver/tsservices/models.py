from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    id_articulo = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['id_articulo'])
        ]