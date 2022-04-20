from unicodedata import category
from django.db import models

# Create your models here.
class News(models.Model):
    #attributes from API
    id = models.CharField(max_length=15)
    publication_date = models.DateTimeField('date published')
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    link = models.CharField(max_length=300)
    #computed attributes
    category = models.CharField(max_length=300)