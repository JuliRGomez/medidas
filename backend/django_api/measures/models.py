from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Measures(models.Model):
    class Meta:
        db_table ='measure_measures'
    reference = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    cm = models.FloatField()
