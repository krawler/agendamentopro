from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.Principal.as_view(), name="principal"),
    path('atualizacliente', views.Atualiza_Cliente.as_view(), name="atualizacliente"),
    path('atualizajson', views.Atualiza_Json.as_view(), name="atualizajson"),
]