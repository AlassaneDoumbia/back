from django.db import models

# '%b %d, %Y',      # 'Oct 25, 2006'

class Pdp_OUT(models.Model):
    Date = models.CharField(max_length=25)
    Operator = models.CharField(max_length=255)
    GTP_C_Procedure_Attempts = models.IntegerField()
    GTP_C_Procedure_Failures = models.IntegerField()
    GTP_C_Procedure_Failure = models.FloatField()
    GTP_C_Procedure_Average_Latency_msec = models.FloatField(null=True)
    Eff_PDP_Act = models.FloatField()
    date_mns = models.BigIntegerField(default=None)
    
    def __str__(self):
        return "Pdp_OUT"

class Pdp_IN(models.Model):
    Date = models.CharField(max_length=25)
    Operator = models.CharField(max_length=255)
    GTP_C_Procedure_Attempts_IN = models.IntegerField()
    GTP_C_Procedure_Failures_IN = models.IntegerField()
    GTP_C_Procedure_Failure_IN = models.FloatField()
    GTP_C_Procedure_Average_Latency_msec_IN = models.FloatField(null=True)
    Eff_PDP_Act_IN = models.FloatField()
    date_mns = models.BigIntegerField(default=None)
    
    def __str__(self):
        return "Pdp_IN"

