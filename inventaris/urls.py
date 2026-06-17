from django.urls import path
from . import views

app_name = 'inventaris'

urlpatterns = [
    path('', views.inventaris_index, name='index'),
]

