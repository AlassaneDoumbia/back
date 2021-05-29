from django.contrib import admin
from import_export import resources
from .models import Bearer_In, Bearer_Out

class Bearer_In_Resource(resources.ModelResource):
    class Meta:
        model = Bearer_In

class Bearer_Out_Resource(resources.ModelResource):
    class Meta:
        model = Bearer_Out