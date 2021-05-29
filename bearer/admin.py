from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Bearer_In, Bearer_Out

@admin.register(Bearer_In)
class Bearer_In_Admin(ImportExportModelAdmin):
    pass

@admin.register(Bearer_Out)
class Bearer_Out_Admin(ImportExportModelAdmin):
    pass