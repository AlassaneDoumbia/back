from django.db import models

# '%b %d, %Y',      # 'Oct 25, 2006'


class Sai_IN(models.Model):
    Interval_Time = models.CharField(max_length=25)
    PLMN_Carrier = models.CharField(max_length=100)
    Direction = models.CharField(max_length=40)
    Service = models.CharField(max_length=20)
    Opcode = models.CharField(max_length=100)
    HVA = models.CharField(max_length=40)
    Total_Transactions = models.PositiveIntegerField()
    Failed_Transactions =models.PositiveIntegerField()
    EFF =  models.PositiveIntegerField()
    date_mns = models.BigIntegerField(default=None)
    
    def __str__(self):
        return "SAI_IN"


class Sai_OUT(models.Model):
    Interval_Time = models.CharField(max_length=255)
    PLMN_Carrier = models.CharField(max_length=255)
    Direction = models.CharField(max_length=255)
    Service = models.CharField(max_length=255)
    Opcode = models.CharField(max_length=255)
    HVA = models.CharField(max_length=255)
    Total_Transactions = models.IntegerField()
    Failed_Transactions =models.IntegerField()
    EFF =models.IntegerField()
    date_mns = models.BigIntegerField(default=None)
    #curl -X PUT -H "Content-Type: application/json" -d '{"EFF":"1","HVA":"221_Senegal Free"}' http://127.0.0.1:8000/sai/1
    def __str__(self):
        return "Sai_OUT"