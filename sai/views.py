from globalP.models import Params
from globalP.views import stringSQL
from globalP.serializers import customSerializer
import os
from io import StringIO

import pandas as pd
from tablib import Dataset
import xlrd
from .models import Sai_IN, Sai_OUT
from sai.serializers import Sai_IN_Serializer, Sai_OUT_Serializer, FileSaiSerializer,ParameterwSaiSerializer
from rest_framework.decorators import api_view, action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
import time


#
# def statsbyDate(transfert_serializer_part):
#     my_list = {}
#     for data in transfert_serializer_part:
#         datestring = data["create_at"]
#         date_time_obj =datetime.datetime.strptime(datestring[:-1], "%Y-%m-%dT%H:%M:%S.%f")
#
#         if str(date_time_obj.date()) in my_list:
#             my_list.update({str(date_time_obj.date()): my_list[str(date_time_obj.date())] + data["montant"]})
#         else:
#             my_list[str(date_time_obj.date())] = data["montant"]
#     return my_list
#
#

class SaiViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Sai_OUT.objects.raw("SELECT parameter1, COUNT(*) FROM statistic_stat GROUP BY parameter1 order by count(*) desc LIMIT 10")
    queryset = Sai_OUT.objects.all()
    serializer_class = Sai_OUT_Serializer
    search_fields = ['^PLMN_Carrier']

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
        
    @action(methods=['get'], detail=False, url_name='attempssai')
    def attempssai(self, request, *args, **kwargs):

        type = kwargs['target_id']
        if type == "out":
            #queryset = Sai_OUT.objects.all()[:1000]
            queryset = Sai_OUT.objects.all()
            razbi = Sai_OUT_Serializer(queryset, many=True)
        else:
            queryset = Sai_IN.objects.all()
            razbi = Sai_IN_Serializer(queryset, many=True)
        my_list = {}
        for data in razbi.data:
            #montan = montan + data["montant"]
            if data["Interval_Time"] in my_list:
                current = my_list[data["Interval_Time"]] + data["EFF"]
                my_list.update({data["Interval_Time"]: current/2})
            else:
                my_list[data["Interval_Time"]] = data["EFF"]

        return Response({"liste": my_list})

    @action(detail=False, methods=['post'], serializer_class=ParameterwSaiSerializer)
    def parametre(self, request, *args, **kwargs):
        serializer = ParameterwSaiSerializer(data=request.data)
        # queryset = Sai_OUT.objects.raw("SELECT EFF, date_mns FROM sai_sai_out WHERE date_mns BETWEEN 1606215600 AND 1606291200")
        # queryset = Sai_OUT.objects.raw("SELECT * FROM sai_sai_out ")
        # razbi = Sai_OUT_Serializer(queryset, many=True) 
        if serializer.is_valid():
            country_operator = serializer.validated_data['country_operator']
            roaming = serializer.validated_data['roaming']
            debut_obj = getDateToMills(serializer.validated_data['dateDebut'])
            fin_obj = getDateToMills(serializer.validated_data['dateFin'])

            if roaming == "out":
                sql = "select substr(Interval_Time,1,12) as date, sum(Total_Transactions) as Total_Transactions, avg(EFF) as EFF from sai_sai_out where PLMN_Carrier='"+str(country_operator)+"' AND date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"' group by date limit 25"
                # sql = "select id, substr(Interval_Time,1,12) as date, sum(Total_Transactions) as Total_Transactions, avg(EFF) as EFF from sai_sai_out where PLMN_Carrier='"+str(country_operator)+"' AND date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"' group by date limit 25"
                queryset = Params.objects.raw(sql)
                # queryset = Sai_OUT.objects.raw("SELECT id, Total_Transactions, Interval_Time, EFF, date_mns FROM sai_sai_out WHERE"+
                # " date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"'")
                #{"roaming":"in","country_operator":"1_Canada Bell Mobility","dateDebut":"Nov 01, 2020 08:00","dateFin":"Nov 15, 2020 08:00"}
                razbi = customSerializer(queryset, many=True)                               

            else:
                sql = "select substr(Interval_Time,1,12) as date, sum(Total_Transactions) as Total_Transactions, avg(EFF) as EFF from sai_sai_in where PLMN_Carrier='"+str(country_operator)+"' AND date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"' group by date limit 25"
                # sql = "select id, substr(Interval_Time,1,12) as date, sum(Total_Transactions) as Total_Transactions, avg(EFF) as EFF from sai_sai_in where PLMN_Carrier='"+str(country_operator)+"' AND date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"' group by date limit 25"
                # queryset = Sai_OUT.objects.raw("SELECT Interval_Time, EFF, date_mns FROM sai_sai_out WHERE PLMN_Carrier="+str(country_operator)+
                queryset = Params.objects.raw(sql)
                # queryset = Sai_IN.objects.filter(PLMN_Carrier=country_operator).filter(Interval_Time__gte=dateDebut).filter(Interval_Time__lte=dateFin)
                razbi = customSerializer(queryset, many=True)
                
            return Response(razbi.data, status=status.HTTP_201_CREATED)
        return Response("Erreur de manipulation, verifier vos donné",status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=FileSaiSerializer)
    def upload(self, request, *args, **kwargs):
        """
         Telecharger le fichier txt envoyer par la dgid pour effectuer une transaction
        """
        print(request.data)
        serializer = FileSaiSerializer(data=request.data)
        if serializer.is_valid():
            i = 3
            uploaded_file = serializer.validated_data['file']
            df = pd.read_excel(uploaded_file.read(), engine="openpyxl")
           
            print(df)
            try:
                liste = []
                if serializer.validated_data['bound'] =="out":                
                    liste = insertData(df, Sai_OUT, "out")
                    # print(Sai_OUT.objects.filter(PLMN_Carrier=country_operator))
                else:
                    liste = insertData(df, Sai_IN, "in")
            except:
                return Response("Erreur de formatage du fichier. Merci de bien effectuer une verification avant l'import",status=status.HTTP_400_BAD_REQUEST)

            return Response({"numberofligne": len(df), "type": df.columns}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def insertData(df, object, roam):
    liste = []
    i = 1
    if roam == "in":
        i = 4
    while i < len(df):
        if roam == "out":
            sai: object = object(
                Interval_Time = df["Date"][i], date_mns = getDateToMills(df["Date"][i]), 
                PLMN_Carrier=df["PLMN Carrier"][i],
                Direction=df["Direction"][i], Service=df["Service"][i],
                Opcode=df["Opcode"][i], HVA=df["HVA"][i], Total_Transactions=df["Total Transactions"][i],
                Failed_Transactions=df["Failed Transactions"][i], EFF=df["Eff "][i],
            )
        else:
            sai: object = object(
                Interval_Time = df["Date"][i], date_mns = getDateToMills(df["Date"][i]), 
                PLMN_Carrier=df["PLMN Carrier"][i],
                Direction=df["Direction"][i], Service=df["Service"][i],
                Opcode=df["Opcode"][i], HVA=df["HVA"][i], Total_Transactions=df["Total Transactions"][i],
                Failed_Transactions=df["Failed Transactions"][i], EFF=df["EFF"][i],
            )
        i = i + 1
        liste.append(sai)
            

    data = object.objects.bulk_create(liste)
    return data

def getDateToMills(date):
    date_time_obj = datetime.strptime(date, '%b %d, %Y')
    # date_time_obj = datetime.strptime(date, '%b %d, %Y %H:%M')
    return int(date_time_obj.timestamp())

def stringSQL(format, debut, fin, carrier ) :
    if format == "heure":
        return "select id, substr(Interval_Time,1,12) as date, substr(Interval_Time,14,18) as heure, sum(Total_Transactions) as Total_Transactions, avg(EFF) as EFF from sai_sai_in where PLMN_Carrier='"+str(carrier)+"' AND date_mns BETWEEN '"+str(debut)+"' AND '"+str(fin)+"' group by date, heure limit 20"
    else:
        return "select id, substr(Interval_Time,1,12) as date, substr(Interval_Time,14,18) as heure, sum(Total_Transactions) as Total_Transactions, avg(EFF) as EFF from sai_sai_in where PLMN_Carrier='"+str(carrier)+"' AND date_mns BETWEEN '"+str(debut)+"' AND '"+str(fin)+"' group by date limit 20"
