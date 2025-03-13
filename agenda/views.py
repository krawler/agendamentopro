from __future__ import annotations
import json
from django.shortcuts import render, redirect
from django.views import View
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from requests import get
from perfil import perfil_service
from .models import Agendamento
from perfil.models import PerfilUsuario
from . import agenda_service
from datetime import datetime, timedelta
from django.contrib import messages
from django.views.generic.list import ListView
from .models import fila_mensagens


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

        user = self.request.user
        agendamentos = Agendamento.objects.filter(profissional=user)   
        agendamentos = serializers.serialize('json', agendamentos)
        context = {
            'agendamentos' : agendamentos,
            'perfis' : PerfilUsuario.objects.all() 
        }

        return render(self.request, 'agenda/agenda.html', context)
    
    
    def post(self, *args, **kwargs):
        hora_inicio      = self.request.POST.get('hora_inicio')
        hora_final       = self.request.POST.get('hora_final')
        data_evento     = self.request.POST.get('data_evento')  
        ultima_atualizacao = self.request.POST.get('ultima_atualizacao')  
        profissional    = self.request.user
        json_event      = self.request.POST.get('jsonEvent')
        id_json_event   = self.request.POST.get('id_evento')
        agendamento = Agendamento.objects.filter(id_jsondiv_evento=id_json_event).first()
        if agendamento is None:
            nova_agenda = agenda_service.Agenda_Service().adiciona_evento(hora_inicio, hora_final, data_evento, profissional, json_event, id_json_event)
            lista_agendas = [nova_agenda]
            json_data = serializers.serialize('json', lista_agendas)
        else:
            agenda = agenda_service.Agenda_Service().atualiza_evento(id_json_event, json_event, hora_inicio, hora_final)
            if agenda is not None:
                lista_agendas = [agenda]
                json_data = serializers.serialize('json', lista_agendas)
            else:
                json_data = '{retorno : false}'    

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
        id_json_evento = self.request.POST.get('id_evento')
        json_evento = self.request.POST.get('jsonEvent')
        agenda_service.Agenda_Service().atualiza_json(id_json_evento, json_evento)
        qs_retorno = Agendamento.objects.filter(data_evento=datetime.today(),
                                                profissional=self.request.user, 
                                                hora_inicio__gte=datetime.now() + timedelta(hours=-3))
        json_retorno = serializers.serialize('json', qs_retorno)
        return JsonResponse(json_retorno, safe=False)

class Atualiza_Evento(DispachLoginRequired, View):
    
     def post(self, *args, **kwargs):
        hora_inicio = self.request.POST.get('hora_inicio')
        hora_final = self.request.POST.get('hora_final')
        id_json_evento = self.request.POST.get('id_evento');
        json_evento = self.request.POST.get('jsonEvent');
        agenda_service.Agenda_Service().atualiza_evento(id_json_evento, json_evento, hora_inicio, hora_final);
        retorno = '{retorno : true}'
        return JsonResponse(retorno, safe=False)

class Marcar(View):
    
    def get(self, *args, **kwargs):
        
        user = self.request.user
        if not user.is_authenticated:
            return redirect('perfil:login')
        data_evento = self.request.GET.get('data_evento')
        if data_evento is None:
            data_evento = datetime.now()
        else:
            data_evento = datetime.strptime(data_evento, "%Y-%m-%d")    
        
        profissional = self.request.GET.get('profissional')
        profissional = User.objects.filter(id=profissional).first()
        
        if profissional is not None:    
            horarios = agenda_service.Agenda_Service().gera_intervalos('09:00', '21:00', data_evento, profissional)
        else:
            horarios = ''
        
        context = {
            'horarios' : horarios,
            'profissionais' : perfil_service.PerfilService().get_profissionais(),
            'profissional_selecionado' : profissional  
        }

        return render(self.request, 'agenda/novo_horario.html', context)
    
    def post(self, *args, **kwargs):
        
        user = self.request.user
        data_evento = self.request.POST.get('data_evento')
        horario_inicio_fim = self.request.POST.get('horario_inicio_fim')
        id_profissional = self.request.POST.get('profissional')
        
        if id_profissional is None or id_profissional == '':
            messages.error(
                    self.request,
                    'Selecione um profissional'
            )
            return redirect('agenda:marcar')
        
        profissional = User.objects.get(id=id_profissional)
        
        agendamento = agenda_service.Agenda_Service().adiciona_evento_formulario(horario_inicio_fim, 
                                                                                 data_evento, 
                                                                                 user, 
                                                                                 profissional)

        agenda_service.Agenda_Service().envia_email(user, 
                                                    profissional, 
                                                    data_evento, 
                                                    horario_inicio_fim, 
                                                    self.request)
        
      #  fila_mensagens[agendamento.id] = agenda_service.Agenda_Service().add_mensagem_fila(user, 
        agenda_service.Agenda_Service().envia_sms(user, data_evento, agendamento, horario_inicio_fim)   
       
        context = {
            'agendamento': agendamento,
        }
        
        return render(self.request, 
                      'agenda/agendamento_concluido.html', 
                      context)


class Tabela(DispachLoginRequired, ListView):
    model = Agendamento
    template_name = 'agenda/tabela.html'
    context_object_name = 'agendamentos'
    ordering = ['-id']
    
    def get(self, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        context = {'agendamentos': self.object_list}
        
        return render(self.request, 
                      self.template_name, 
                      context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     agendamentos = context['agendamentos']
    #     for agendamento in agendamentos:     
    #         if agendamento.pessoa is not None:       
    #             perfil = agendamento.pessoa.perfilusuario
    #             agendamento.perfil_data = perfil
    #     context['agendamentos'] = agendamentos
    #     return context


class Mensagens(View):
    
    def get(self, *args, **kwargs):
        mensagens = fila_mensagens.values()
        json_data = serializers.serialize('json', mensagens)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)


class Atualiza_Sms(View):

    def get(self, *args, **kwargs):
        agendamento_id = self.request.GET.get('agendamento_id')
        if agendamento_id is not None:
            try:
                agendamento_id = int(agendamento_id)
                if agendamento_id in fila_mensagens:
                    fila_mensagens.pop(agendamento_id)
                    return JsonResponse({'message': 'Agendamento removido da fila'}, safe=False)
            except ValueError:
                return JsonResponse({'message': 'Erro ao remover agendamento, valor inválido'}, safe=False)
    
        return JsonResponse({'message': 'Agendamento não foi removido da fila'}, safe=False)
    