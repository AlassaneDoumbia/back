from rest_framework import serializers
from bearer.models import Bearer_In, Bearer_Out


class Bearer_In_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Bearer_In
        fields = '__all__'


class Bearer_OUT_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Bearer_Out
        fields = '__all__'

"""Verify"""
class ParameterwBearerSerializer(serializers.Serializer):
    roaming = serializers.CharField(required=True)
    country_operator = serializers.CharField(required=True)
    dateDebut = serializers.CharField(required=True)
    dateFin = serializers.CharField(required=True)

class FileBearerSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    inputFile = serializers.FileField(max_length=None, required=True)