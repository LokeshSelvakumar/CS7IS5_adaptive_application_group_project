from django.db import models

# Create your models here.
class Stocks(models.Model):
    name = models.CharField()
    price = models.FloatField()