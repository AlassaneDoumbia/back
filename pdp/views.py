from globalP.views import stringSQL
from globalP.models import Params
from globalP.serializers import FileSerializer, customSerializer
import os
import re
from io import StringIO

import pandas as pd
from tablib import Dataset
import xlrd
from .models import Pdp_IN, Pdp_OUT
from pdp.serializers import FilePdpSerializer, ParameterwPdpSerializer, Pdp_IN_Serializer, Pdp_OUT_Serializer  
from rest_framework.decorators import api_view, action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from datetime import datetime
import time



#####################################################################
#####################################################################
class PdpViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Pdp_IN.objects.all()
    # queryset = Pdp_IN.objects.raw("SELECT * FROM statistic_stat GROUP BY parameter1 order by count(*) desc LIMIT 10")
    serializer_class = Pdp_IN_Serializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], serializer_class=ParameterwPdpSerializer)
    def parametre(self, request, *args, **kwargs):
        serializer = ParameterwPdpSerializer(data=request.data)
        if serializer.is_valid():
            country_operator = serializer.validated_data['country_operator']
            roaming = serializer.validated_data['roaming']
            debut_obj = getDateToMills(serializer.validated_data['dateDebut'].replace(" 08:00",""))
            fin_obj = getDateToMills(serializer.validated_data['dateFin'].replace(" 08:00",""))
            # sql = stringSQL("heure",debut_obj,fin_obj, country_operator)
            # print(sql)
            if roaming == "out":
                sql = "select id, Date as date, GTP_C_Procedure_Attempts as Total_Transactions, GTP_C_Procedure_Average_Latency_msec as heure, Eff_PDP_Act as EFF from pdp_pdp_out  where date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"'limit 30;"
                queryset = Params.objects.raw(sql)
                razbi = customSerializer(queryset, many=True)                               

            else:
                sql = "select id, Date as date, GTP_C_Procedure_Attempts_IN as Total_Transactions, GTP_C_Procedure_Average_Latency_msec_IN as heure, Eff_PDP_Act_IN as EFF from pdp_pdp_in where date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"'limit 30;"
                queryset = Params.objects.raw(sql)
                razbi = customSerializer(queryset, many=True)


            return Response(razbi.data, status=status.HTTP_201_CREATED)
        return Response("Erreur de manipulation, verifier vos donné",status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=FileSerializer)
    def upload(self, request, *args, **kwargs):
        """
         Telecharger le fichier txt envoyer par la dgid pour effectuer une transaction
        """
        print(request.data)
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            df = pd.read_excel(uploaded_file.read(), engine="openpyxl")
           
            print(df)
    
            liste = []
            if serializer.validated_data['bound'] =="out":                
                liste = insertData(df, Pdp_OUT, "out")
            else:
                liste = insertData(df, Pdp_IN, "in")


            return Response({"numberofligne": len(df), "type": df.columns}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



def insertData(df, object, roam):
    liste = []
    i = 1
    while i < len(df): 
        if roam == "out":
            pdp: object = object(
                Operator=df["Operator"][i], date_mns = getDateToMills(df["Date"][i]), 
                GTP_C_Procedure_Attempts=checkValue(df["GTP-C Procedure Attempts"][i]), Eff_PDP_Act=checkValue(df["Eff PDP Act"][i]),
                GTP_C_Procedure_Failure =checkValue(df["GTP-C Procedure Failure %"][i]), 
                GTP_C_Procedure_Average_Latency_msec=checkValue(df["GTP-C Procedure Average Latency (msec)"][i]), 
                GTP_C_Procedure_Failures=checkValue(df["GTP-C Procedure Failures"][i]),Date= df["Date"][i]
            )
        else:
            pdp: object = object(
                Operator=df["Operator"][i], date_mns = getDateToMills(df["Date"][i]), 
                GTP_C_Procedure_Attempts_IN=int(checkValue(df["GTP-C Procedure Attempts IN"][i])), Eff_PDP_Act_IN=checkValue(df["Eff PDP Act IN"][i]),
                GTP_C_Procedure_Failure_IN =checkValue(df["GTP-C Procedure Failure % IN"][i]), 
                GTP_C_Procedure_Average_Latency_msec_IN=checkValue(df["GTP-C Procedure Average Latency (msec) IN"][i]), 
                GTP_C_Procedure_Failures_IN=int(checkValue(df["GTP-C Procedure Failures IN"][i])),Date= df["Date"][i]
            )
        i = i + 1
        liste.append(pdp)           

    data = object.objects.bulk_create(liste)
    return data


def getDateToMills(date):
    # date_time_obj = datetime.strptime(date, '%b %d, %Y %H:%M')
    date_time_obj = datetime.strptime(date, '%b %d, %Y')
    return int(date_time_obj.timestamp())


def checkValue(val):
    # if val == "NaN":
    if isfloat(val):
        return val
    return 0


def isfloat(value):
  try:
    int(value)
    return True
  except ValueError:
    return False