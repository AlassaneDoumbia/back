from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Sai_IN, Sai_OUT

@admin.register(Sai_IN)
class SaiAdmin(ImportExportModelAdmin):
    pass


@admin.register(Sai_OUT)
class SaiAdmin(ImportExportModelAdmin):
    pass