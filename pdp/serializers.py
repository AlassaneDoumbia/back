from rest_framework import serializers
from .models import Pdp_IN, Pdp_OUT 


class Pdp_IN_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Pdp_IN
        fields = '__all__'


class Pdp_OUT_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Pdp_OUT
        fields = '__all__'


"""Verify"""
class ParameterwPdpSerializer(serializers.Serializer):
    roaming = serializers.CharField(required=True)
    country_operator = serializers.CharField(required=True)
    dateDebut = serializers.CharField(required=True)
    dateFin = serializers.CharField(required=True)

class FilePdpSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    inputFile = serializers.FileField(max_length=None, required=True)