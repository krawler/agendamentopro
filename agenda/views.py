from django.shortcuts import render
from django.views import View
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from .models import Agendamento
from perfil.models import PerfilUsuario
from . import agenda_service
from datetime import datetime

class Principal(View):
    
    def get(self, *args, **kwargs):
        
        context = {
            'agendamentos' : Agendamento.objects.filter(data_evento=datetime.today()),
            'perfis' : PerfilUsuario.objects.all() 
        }

        return render(self.request, 'agenda/agenda.html', context)
    
    
    def post(self, *args, **kwargs):
        hora_inicio = self.request.POST.get('hora_inicio')
        hora_final = self.request.POST.get('hora_final')
        data_evento = self.request.POST.get('data_evento')  
        ultima_atualizacao = self.request.POST.get('ultima_atualizacao')  
        profissional = self.request.user
        
        nova_agenda = agenda_service.Agenda_Service().adiciona_evento(hora_inicio, hora_final, data_evento, profissional)
        lista_agendas = [nova_agenda]
        json_data = serializers.serialize('json', lista_agendas)
        return JsonResponse(json_data, safe=False)

class Atualiza_Cliente(View):
    
     def post(self, *args, **kwargs):
        perfil_id = self.request.POST.get('perfil_id');
        evento_id = self.request.POST.get('evento_id');
        user_perfil_pessoa = PerfilUsuario.objects.filter(id=perfil_id).first()
        qs_agendamento = Agendamento.objects.filter(id=evento_id)
        agendamento = qs_agendamento.first()
        agendamento.pessoa = user_perfil_pessoa.usuario
        agendamento.save()
        json_data = serializers.serialize('json', qs_agendamento)
        return JsonResponse(json_data, safe=False)