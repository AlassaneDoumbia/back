import datetime
import requests

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from bearer.models import Bearer_Out, Bearer_In
from bearer.serializers import Bearer_OUT_Serializer, Bearer_In_Serializer
from globalP.models import Countries
from globalP.serializers import CountriesSerializer
from pdp.models import Pdp_OUT, Pdp_IN
from pdp.serializers import Pdp_OUT_Serializer, Pdp_IN_Serializer
from sai.models import Sai_OUT, Sai_IN
from sai.serializers import Sai_OUT_Serializer, Sai_IN_Serializer


def statsbyDate(transfert_serializer_part):
    my_list = {}
    for data in transfert_serializer_part:
        datestring = data["create_at"]
        date_time_obj =datetime.datetime.strptime(datestring[:-1], "%Y-%m-%dT%H:%M:%S.%f")

        if str(date_time_obj.date()) in my_list:
            my_list.update({str(date_time_obj.date()): my_list[str(date_time_obj.date())] + data["montant"]})
        else:
            my_list[str(date_time_obj.date())] = data["montant"]
    return my_list


@api_view(['GET'])
def statistiquesView(request, format=None):
    """
     recevoir les statistiques concernant les donnees de transfert
    """
    # transfert_count = len(Transfert.objects.all())
    # compte_count = len(Compte.objects.all())
    # serializer_part = CompteSerializer(Compte.objects.all(), many=True).data
    # transfert_serializer_part = TransfertSerializer(Transfert.objects.all(), many=True).data
    # transfert_order_serializer_part = TransfertSerializer(Transfert.objects.all().order_by("-create_at"), many=True).data
    # globalmontant = sommeTotal(serializer_part)
    # lastTransfert_serialize = TransfertSerializer(Transfert.objects.all().order_by("-create_at")[:5], many=True).data
    # top3Transfert_serialize = TransfertSerializer(Transfert.objects.all().order_by("-montant")[:3], many=True).data
    # user_serialize = UserSerializer(User.objects.all().order_by("date_joined")[:5], many=True).data
    # my_list = {}
    # valuesTab = []
    # #listeByDate = statsbyDate(transfert_serializer_part)
    # montan=0
    # for data in transfert_order_serializer_part:
    #     montan = montan + data["montant"]
    #     valuesTab.append(data["montant"])
    #     if data["originalName"] in my_list:
    #         my_list.update({data["originalName"]: my_list[data["originalName"]] + data["montant"]})
    #     else:
    #         my_list[data["originalName"]] = data["montant"]
    # print(my_list)
    # listeByDate = statsbyDate(transfert_serializer_part)
    total_account = 0
    # return Response({"nbreTransfert": transfert_count, "globalmontant": globalmontant, "byDate": listeByDate,
    #                  "liste": my_list, "valuesTab": valuesTab, "lastTransfert": lastTransfert_serialize,
    #                  "userList": user_serialize, "top3": top3Transfert_serialize,})
    #return HttpResponse(transfert_count)@api_view(['GET'])

@api_view(['GET'])
def homedataFunctionView(request, format=None):
    """
     get all statistiques for home
    """

    #snippets = Bearer.objects.all()[:20]
    serializer_bearer_out = Bearer_OUT_Serializer(Bearer_Out.objects.all(), many=True)
    serializer_bearer_in = Bearer_In_Serializer(Bearer_In.objects.all(), many=True)
    serializer_pdp_out = Pdp_OUT_Serializer(Pdp_OUT.objects.all(), many=True)
    serializer_pdp_in = Pdp_IN_Serializer(Pdp_IN.objects.all(), many=True)
    serializer_sai_out = Sai_OUT_Serializer(Sai_OUT.objects.all(), many=True)
    serializer_sai_in = Sai_IN_Serializer(Sai_IN.objects.all(), many=True)


    attempsbearerIN: int = attemps(serializer_bearer_in.data, "bearer_in")
    attempsbearerOUT: int  = attemps(serializer_bearer_out.data, "bearer_out")

    attempspdpOUT: int  = attemps(serializer_pdp_out.data, "pdp_out")
    attempspdpIN : int = attemps(serializer_pdp_in.data, "pdp_in")

    attempssaiOUT: int  = attemps(serializer_sai_out.data, "sai_out")
    attempssaiIN: int  = attemps(serializer_sai_in.data, "sai_in")

    total = attempsbearerIN + attempsbearerOUT + attempspdpOUT + attempspdpIN + attempssaiOUT + attempssaiIN
    totalIN = attempsbearerIN + attempspdpIN + attempssaiIN
    totalOUT = attempsbearerOUT + attempspdpOUT + attempssaiOUT
    totalFailed = attempsFailed(serializer_sai_in.data, serializer_sai_out.data, serializer_pdp_out.data, serializer_pdp_in.data,
                                serializer_bearer_in.data, serializer_bearer_out.data)
    # transfert_serializer_part = TransfertSerializer(Transfert.objects.all(), many=True).data
    # lastTransfert_serialize = UserSerializer(User.objects.all().order_by("date_joined")[:5], many=True).data
    # my_list = {}
    return Response({"attempsbearerIN": attempsbearerIN, "attempsbearerOUT": attempsbearerOUT,
                     "attempspdpOUT": attempspdpOUT, "attempspdpIN": attempspdpIN,
                     "attempssaiOUT": attempssaiOUT, "attempssaiIN": attempssaiIN,
                     "total": total, "totalIN": totalIN, "totalOUT": totalOUT, "totalFailed": totalFailed,
                     })

@api_view(['GET','POST'])
def countryFunctionView(request, format=None):
    """
     test different function before implementation
    """

    if request.method == 'GET':
        countries = CountriesSerializer(Countries.objects.all(), many=True).data

        return Response({"data": countries}, status=status.HTTP_200_OK)

    # if request.method == 'POST':
    #     response = requests.get("https://restcountries.eu/rest/v2/all")
    #     answer = response.json()
    #     liste = []
    #     for item in answer:
    #
    #         countrie: Countries = Countries(
    #             nom=item['name'], alpha3Code =item['name'], flag=item['flag'],
    #             callingCodes=item['callingCodes'][0], capital=item['capital'], region=item['region'],
    #         )
    #         countrie.save()
    #         liste.append(countrie)
    #
    #     country_serialized = CountriesSerializer(liste, many=True).data
    #
    #     return Response({"data": country_serialized}, status=status.HTTP_200_OK)
    my_list = {}
    #return Response({"userList": answer,})


def attemps(liste, type):
    attemps = 0
    for item in liste:
        if type == "bearer_out":
            attemps += int(item['GTPv2_C_Attempts_OUT'])

        if type == "bearer_in":
            attemps += int(item['GTPv2_C_Attempts_IN'])

        if type == "pdp_out":
            attemps += int(item['GTP_C_Procedure_Attempts'])

        if type == "pdp_in":
            attemps += int(item['GTP_C_Procedure_Attempts_IN'])

        if type == "sai_out":
            attemps += int(item['Total_Transactions'])

        if type == "sai_in":
            attemps += int(item['Total_Transactions'])

    return attemps

def attempsFailed(listeSAIIN, listeSAIOUT, listePDPIN, listePDPOUT, listeBEARIN, listeBEAROUT):
    attemps = 0
    for item in listeSAIIN:
        attemps += int(item['Failed_Transactions'])

    for item in listeSAIOUT:
        attemps += int(item['Failed_Transactions'])

    for item in listePDPIN:
        attemps += int(item['GTP_C_Procedure_Failures_IN'])

    for item in listePDPOUT:
        attemps += int(item['GTP_C_Procedure_Failures'])

    for item in listeBEARIN:
        attemps += int(item['GTPv2_C_Failures_IN'])

    for item in listeBEAROUT:
        attemps += int(item['GTPv2_C_Failures_OUT'])

    return attemps

# queryset = Sai_OUT.objects.raw("SELECT EFF, date_mns FROM sai_sai_out WHERE date_mns BETWEEN 1606215600 AND 1606291200")
# queryset = Sai_OUT.objects.raw("SELECT Interval_Time, EFF, date_mns FROM sai_sai_out WHERE PLMN_Carrier="+str(country_operator)+
# queryset = Sai_OUT.objects.raw("SELECT id, Total_Transactions, Interval_Time, EFF, date_mns FROM sai_sai_out WHERE"+
# " date_mns BETWEEN '"+str(debut_obj)+"' AND '"+str(fin_obj)+"'")
        
def stringSQL(format, debut, fin, carrier ) :
    if format == "heure":
        return "select id, substr(Interval_Time,1,12) as date, substr(Interval_Time,14,18) as heure, sum(Total_Transactions) as Total_Transactions, avg(EFF) as EFF from sai_sai_in where PLMN_Carrier='"+str(carrier)+"' AND date_mns BETWEEN '"+str(debut)+"' AND '"+str(fin)+"' group by date, heure limit 20"
    else:
        return "select id, substr(Interval_Time,1,12) as date, substr(Interval_Time,14,18) as heure, sum(Total_Transactions) as Total_Transactions, avg(EFF) as EFF from sai_sai_in where PLMN_Carrier='"+str(carrier)+"' AND date_mns BETWEEN '"+str(debut)+"' AND '"+str(fin)+"' group by date limit 20"

