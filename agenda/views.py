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
        id_json_event = self.request.POST.get('id_evento')
        print(id_json_event)
        nova_agenda = agenda_service.Agenda_Service().adiciona_evento(hora_inicio, hora_final, data_evento, profissional, json_event, id_json_event)
        lista_agendas = [nova_agenda]
        json_data = serializers.serialize('json', lista_agendas)

        return JsonResponse(json_data, safe=False)

class Atualiza_Cliente(DispachLoginRequired, View):
    
     def post(self, *args, **kwargs):
        perfil_id = self.request.POST.get('perfil_id');
        evento_id = self.request.POST.get('evento_id');
        qs_agendamento = agenda_service.Agenda_Service().atualiza_cliente(perfil_id, evento_id);
        json_data = serializers.serialize('json', qs_agendamento)
        return JsonResponse(json_data, safe=False)

class Atualiza_Json(DispachLoginRequired, View):
    
     def post(self, *args, **kwargs):
        id_json_evento = self.request.POST.get('id_evento');
        json_evento = self.request.POST.get('jsonEvent');
        qs_evento = agenda_service.Agenda_Service().atualiza_json(id_json_evento, json_evento);
        retorno = '{retorno : true}'
        return JsonResponse(retorno, safe=False)


class Atualiza_Evento(DispachLoginRequired, View):
    
     def post(self, *args, **kwargs):
        hora_inicio = self.request.POST.get('hora_inicio')
        hora_final = self.request.POST.get('hora_final')
        id_json_evento = self.request.POST.get('id_evento');
        json_evento = self.request.POST.get('jsonEvent');
        qs_evento = agenda_service.Agenda_Service().atualiza_evento(id_json_evento, json_evento, hora_inicio, hora_final);
        retorno = '{retorno : true}'
        return JsonResponse(retorno, safe=False)

