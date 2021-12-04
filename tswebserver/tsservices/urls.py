from django.urls import path
from . import views

app_name = 'tsservices'

urlpatterns = [
    path('main/', views.homeforescast, name='homeapp'),
]
