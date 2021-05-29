from globalP.models import Params
from globalP.serializers import FileSerializer, customSerializer
import os
from io import StringIO

import pandas as pd
from .models import Bearer_In, Bearer_Out
from bearer.serializers import Bearer_In_Serializer, Bearer_OUT_Serializer, FileBearerSerializer, ParameterwBearerSerializer 
from rest_framework.decorators import api_view, action
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from datetime import datetime

#####################################################################
class BearerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Bearer_Out.objects.all()
    serializer_class = Bearer_OUT_Serializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], serializer_class=ParameterwBearerSerializer)
    def parametre(self, request, *args, **kwargs):
        serializer = ParameterwBearerSerializer(data=request.data)
        if serializer.is_valid():
            debut_obj = getDateToMills(serializer.validated_data['dateDebut'].replace(" 08:00",""))
            fin_obj = getDateToMills(serializer.validated_data['dateFin'].replace(" 08:00",""))
            country_operator = serializer.validated_data['country_operator']
            roaming = serializer.validated_data['roaming']
            print(debut_obj)
            print(fin_obj)
            

            if roaming == "out":
                sql = "select id, Date as date, GTPv2_C_Attempts_OUT as Total_Transactions, GTPv2_C_Average_Session_Duration_msec_OUT as heure, Efficacité_OUT as EFF from bearer_bearer_out where Opérateur='"+country_operator+"' AND date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"'limit 30 "
                queryset = Params.objects.raw(sql)
                razbi = customSerializer(queryset, many=True)
            else:
                sql = "select id, select Date as date, GTPv2_C_Attempts_IN as Total_Transactions, GTPv2_C_Average_Session_Duration_msec_IN as heure, Efficacité_IN as EFF  from bearer_bearer_in where Opérateur='"+country_operator+"' AND date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"'limit 30 "
                queryset = Params.objects.raw(sql)
                razbi = customSerializer(queryset, many=True)

            return Response(razbi.data, status=status.HTTP_201_CREATED)
        return Response("Erreur de manipulation, verifier vos donné",status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], serializer_class=FileSerializer)
    def upload(self, request, *args, **kwargs):
        """
         Telecharger le fichier txt envoyer par la dgid pour effectuer une transaction
        """
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            df = pd.read_excel(uploaded_file.read(), engine="openpyxl")
            print(df)
            liste = []
            if serializer.validated_data['bound'] =="out":
                liste = insertData(df, Bearer_Out, "out")
            else:
                liste = insertData(df, Bearer_In, "in")


            return Response({"numberofligne": len(liste), "type": df.columns}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def insertData(df, object, roam):
    liste = []
    i = 1
    while i < len(df): 
        if roam == "out":
            bearer: object = object(
                date_mns = getDateToMills(df["Date"][i]),Date= df["Date"][i],Opérateur=df["Opérateur"][i],
                GTPv2_C_Attempts_OUT=int(checkValue(df["GTPv2-C Attempts OUT"][i])), GTPv2_C_Failures_OUT=int(checkValue(df["GTPv2-C Failures OUT"][i])),
                GTPv2_C_Failure_OUT=checkValue(df["GTPv2-C Failure OUT %"][i]), GTPv2_C_Average_Latency_msec_OUT=checkValue(df["GTPv2-C Average Latency (msec) OUT"][1]),
                GTPv2_C_Average_Session_Duration_msec_OUT=df["GTPv2-C Average Session Duration (msec) OUT"][i],
                Efficacité_OUT=checkValue(df["Efficacité OUT"][i]),
            )
        else:
            bearer: object = object(
                date_mns = getDateToMills(df["Date"][i]),Date= df["Date"][i],Opérateur=df["Opérateur"][i],
                GTPv2_C_Attempts_IN=int(checkValue(df["GTPv2-C Attempts IN"][i])), GTPv2_C_Failures_IN=int(checkValue(df["GTPv2-C Failures IN"][i])),
                GTPv2_C_Failure_IN=checkValue(df["GTPv2-C Failure IN %"][i]), GTPv2_C_Average_Latency_msec_IN=(checkValue(df["GTPv2-C Average Latency (msec) IN"][i])),
                GTPv2_C_Average_Session_Duration_msec_IN=df["GTPv2-C Average Session Duration (msec) IN"][i],
                Efficacité_IN=checkValue(df["Efficacité IN"][i]),
        )
        i = i + 1
        liste.append(bearer)           

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