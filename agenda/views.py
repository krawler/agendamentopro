from django.shortcuts import render, redirect
from django.views import View
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from .models import Agendamento
from perfil.models import PerfilUsuario
from . import agenda_service
from datetime import datetime


class DispachLoginRequired(View):
    
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("perfil:login")
    
        return super().dispatch(*args, **kwargs)
    
    def get_query_set(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs


class Principal(DispachLoginRequired, View):
    
    def get(self, *args, **kwargs):

        agendamentos = Agendamento.objects.exclude(json_evento='criado fora do calendario agendador')    
        agendamentos = serializers.serialize('json', agendamentos)
        context = {
            'agendamentos' : agendamentos,
            'perfis' : PerfilUsuario.objects.all() 
        }

        return render(self.request, 'agenda/agenda.html', context)
    
    
    def post(self, *args, **kwargs):
        hora_inicio = self.request.POST.get('hora_inicio')
        hora_final = self.request.POST.get('hora_final')
        data_evento = self.request.POST.get('data_evento')  
        ultima_atualizacao = self.request.POST.get('ultima_atualizacao')  
        profissional = self.request.user
        json_event = self.request.POST.get('jsonEvent')
        print('json event ' + json_event)
        nova_agenda = agenda_service.Agenda_Service().adiciona_evento(hora_inicio, hora_final, data_evento, profissional, json_event)
        lista_agendas = [nova_agenda]
        json_data = serializers.serialize('json', lista_agendas)

        return JsonResponse(json_data, safe=False)

class Atualiza_Cliente(DispachLoginRequired, View):
    
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
