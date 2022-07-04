from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('onetime/', include('onetimesecret.urls')),
    path('onety/', include('onety.urls'))
]
