from django.urls import path

from . import views

urlpatterns = [
    path('', views.generate_data, name='generate_data'),
]
