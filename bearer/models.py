from django.db import models



class Bearer_In(models.Model):
    id = models.BigAutoField(primary_key=True)
    Date = models.CharField(max_length=255)
    Opérateur = models.CharField(max_length=255)
    GTPv2_C_Attempts_IN = models.IntegerField()
    GTPv2_C_Failures_IN = models.IntegerField()
    GTPv2_C_Failure_IN = models.FloatField()
    GTPv2_C_Average_Latency_msec_IN = models.FloatField()
    GTPv2_C_Average_Session_Duration_msec_IN = models.CharField(max_length=255)
    Efficacité_IN = models.FloatField()
    date_mns = models.BigIntegerField(default=None)
   
    def __str__(self):
        return "Bearer_In"

class Bearer_Out(models.Model):
    id = models.BigAutoField(primary_key=True)
    Date = models.CharField(max_length=255)
    Opérateur = models.CharField(max_length=255)
    GTPv2_C_Attempts_OUT = models.IntegerField()
    GTPv2_C_Failures_OUT = models.IntegerField()
    GTPv2_C_Failure_OUT = models.FloatField()
    GTPv2_C_Average_Latency_msec_OUT = models.FloatField()
    GTPv2_C_Average_Session_Duration_msec_OUT = models.CharField(max_length=255)
    Efficacité_OUT = models.FloatField()
    date_mns = models.BigIntegerField(default=None)
   
    def __str__(self):
        return "Bearer_Out"

