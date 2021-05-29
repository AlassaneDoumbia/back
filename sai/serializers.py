from rest_framework import serializers
from sai.models import Sai_IN, Sai_OUT


class Sai_IN_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sai_IN
        fields = '__all__'


class Sai_OUT_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sai_OUT
        fields = '__all__'



class ParameterwSaiSerializer(serializers.Serializer):
    roaming = serializers.CharField(required=True)
    country_operator = serializers.CharField(required=True)
    dateDebut = serializers.CharField(required=True)
    dateFin = serializers.CharField(required=True)

class FileSaiSerializer(serializers.Serializer):
    bound = serializers.CharField(required=True)
    file = serializers.FileField(max_length=None, required=True)