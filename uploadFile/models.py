from django.db import models 
from django.db.models import When

def generate_filename(filename):
  print("blabla")
  return "files/%s/" % (filename)


class File(models.Model):
  id = models.BigAutoField(primary_key=True)
  CHOICE = (("IN","IN"), ("OUT", "OUT"))
  fileName = models.CharField(max_length=100)
  Type = models.CharField(max_length=20, choices=CHOICE)
  files = models.FileField(upload_to="files")
  timestamp = models.DateTimeField(auto_now_add=True)

