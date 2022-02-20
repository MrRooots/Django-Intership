from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import AnimalPhotoView, AnimalsView

urlpatterns = [
  path('', csrf_exempt(AnimalsView.as_view())),
  
  path('<str:animal_id>/photo/', csrf_exempt(AnimalPhotoView.as_view())),
  
  path('<str:animal_id>/photo/<str:filename>', csrf_exempt(AnimalPhotoView.as_view()), name='get_photo')
]