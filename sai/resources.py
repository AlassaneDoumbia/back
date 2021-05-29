from import_export import resources
from .models import Sai_IN, Sai_OUT

class SaiResource(resources.ModelResource):
    class Meta:
        model = Sai_IN


class Sai_OUT_Resource(resources.ModelResource):
    class Meta:
        model = Sai_OUT