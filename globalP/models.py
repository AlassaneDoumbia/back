from django.db import models

# Create your models here.


class Countries(models.Model):
    nom = models.CharField(max_length=255)
    alpha3Code = models.CharField(max_length=255)
    callingCodes = models.CharField(max_length=255)
    capital = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    flag = models.URLField(max_length=255)

    def __str__(self):
        return self.nom



class Params(models.Model):
    date = models.CharField(max_length=100)
    heure = models.CharField(max_length=100)
    # Interval_Time = models.CharField(max_length=100)
    Total_Transactions = models.PositiveIntegerField()
    # Failed_Transactions =models.PositiveIntegerField()
    EFF =  models.FloatField()
    # date_mns = models.BigIntegerField(default=None)
 