from django.contrib import admin
from django.urls import include, path

urlpatterns = [
  path('pets/', include('core.urls'))
]
