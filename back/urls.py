"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from schema_graph.views import Schema
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions, routers
from testapi import views
from sai.views import SaiViewSet
from bearer.views import BearerViewSet
from pdp.views import PdpViewSet
#import globalP

schema_view = get_schema_view(
   openapi.Info(
      title="Digidex portail API",
      default_version='v1',
      description="This APi have been made for Digidex design",
      contact=openapi.Contact(email="doumbialassane10@@gmail.com"),
      license=openapi.License(name="Personal License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'sai', SaiViewSet)
router.register(r'bearer', BearerViewSet)
router.register(r'pdp', PdpViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('ping/', views.ping),
    path('connexion/', views.connectionFunctionView),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^docs/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^docs/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #url(r'^media/images/avatar/$', include('media'), {'document_root': settings.MEDIA_ROOT, }),
    path('schema/', Schema.as_view()),
    path('admin/', admin.site.urls),
    path('', include('uploadFile.urls')),
    #path('countries/', globalP.views.countryFunctionView, name='country'),
    #path('homestats/', globalP.views.homedataFunctionView, name='home_stats'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)