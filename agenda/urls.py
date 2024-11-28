from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.Principal.as_view(), name="principal"),
    #path('concluido/', views.Cadastro_concluido.as_view(), name="cadastro_concluido"),
]