from django.contrib import admin
from .models import File
from uploadFile import models

# Register your models here.

admin.site.register(models.File)

