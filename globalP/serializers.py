from sai.models import Sai_OUT
from rest_framework import serializers
from globalP.models import Countries, Params


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ['nom', 'alpha3Code', 'callingCodes', 'capital', 'region', 'flag']


class customSerializer(serializers.ModelSerializer):
    class Meta:
        model = Params
        fields = ['date', 'heure', 'EFF', 'Total_Transactions']


class FileSerializer(serializers.Serializer):
    bound = serializers.CharField(required=True)
    file = serializers.FileField(max_length=None, required=True)