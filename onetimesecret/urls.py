from django.urls import path
from .views import *

urlpatterns = [
    path('', OneTimeRequest.as_view())
]
