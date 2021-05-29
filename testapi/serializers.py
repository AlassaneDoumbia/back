from django.contrib.auth.models import Group
from rest_framework import serializers
# from testapi.models import User


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['first_name', 'username', 'last_name', 'matricule']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

