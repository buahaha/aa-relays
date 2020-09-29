from django.urls import path
from . import views


app_name = 'aarelays'

urlpatterns = [
    path('', views.index, name='index'),
]