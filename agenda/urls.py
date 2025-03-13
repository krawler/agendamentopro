from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.Principal.as_view(), name="principal"),
    path('atualizacliente', views.Atualiza_Cliente.as_view(), name="atualizacliente"),
    path('atualizajson', views.Atualiza_Json.as_view(), name="atualizajson"),
    path('atualizaevento', views.Atualiza_Evento.as_view(), name="atualizaevento"),
    path('marcar', views.Marcar.as_view(), name="marcar"),
    path('tabela', views.Tabela.as_view(), name="tabela"),
    path('mensagens', views.Mensagens.as_view(), name="mensagens"),
    path('atualizasms', views.Atualiza_Sms.as_view(), name="atualizasms"),
]