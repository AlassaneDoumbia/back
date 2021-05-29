from rest_framework import serializers
from uploadFile.models import File


class FileSerializer(serializers.ModelSerializer):
  class Meta:
    model = File
    fields ="__all__"
