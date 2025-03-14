import json
import random
import string
import requests
import json

from agenda.email.py_email import PyEmail
from agenda.whatsapp import py_whatsapp
from perfil.models import PerfilUsuario
from .models import Agendamento
from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import User
from django.db.models import Q


class Agenda_Service():

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Agenda_Service, cls).__new__(cls)
        return cls.instance    


    def adiciona_evento(self, dt_inicio, dt_final, data_evento, profissional, json_event, id_jsondiv_evento):
        
        data_evento = datetime.strptime(data_evento, '%Y-%m-%d')
        hora_inicio = datetime.strptime(dt_inicio, '%H:%M:%S')
        hora_final = datetime.strptime(dt_final, '%H:%M:%S')

        agenda = Agendamento(pessoa=None,
                            profissional=profissional, 
                            data_evento=data_evento, 
                            hora_inicio=hora_inicio, 
                            hora_final=hora_final,
                            json_evento=json_event,
                            id_jsondiv_evento=id_jsondiv_evento)
        agenda.save()

        return agenda

    def adiciona_evento_formulario(self, hora_inicio_fim, data_evento, usuario, profissional):
        
        id_jsondiv_evento = self.gerar_string_aleatoria()
        
        data_evento = datetime.strptime(data_evento, '%Y-%m-%d')
        tupla_horarios = eval(hora_inicio_fim)
        horario_inicio = tupla_horarios[0]
        horario_fim = tupla_horarios[1]
        
        json_event = self.create_json_evento(usuario.username,  
                                             data_evento.day,                                       
                                             data_evento.month,                                              
                                             data_evento.year, 
                                             horario_inicio, 
                                             horario_fim, 
                                             id_jsondiv_evento)
        hora_inicio = datetime.strptime(f"{data_evento.year}-{data_evento.month}-{data_evento.day} {horario_inicio}", "%Y-%m-%d %H:%M")

        hora_final = datetime.strptime(f"{data_evento.year}-{data_evento.month}-{data_evento.day} {horario_fim}", "%Y-%m-%d %H:%M")
        #datetime_horario_fim = data_evento.strptime(horario_fim, '%H:%M')
        #datetime_horario_fim = datetime_horario_fim + timedelta(hours=+3)
        agenda = Agendamento(pessoa=usuario,
                             profissional=profissional, 
                             data_evento=hora_inicio.date(), 
                             hora_inicio=hora_inicio, 
                             hora_final=hora_final,
                             json_evento=json_event,
                             id_jsondiv_evento=id_jsondiv_evento)
        agenda.save()

        return agenda

    
    def atualiza_evento(self, json_event, id_jsondiv_evento, dt_inicio, dt_final):
        
        data_evento = datetime.now()
        hora_inicio = datetime.strptime(dt_inicio, '%H:%M:%S')
        hora_final = datetime.strptime(dt_final, '%H:%M:%S')

        agendamento = Agendamento.objects.filter(id_jsondiv_evento=id_jsondiv_evento).first()
        if agendamento is not None:
            agendamento.hora_inicio = hora_inicio
            agendamento.hora_final = hora_final
            agendamento.json_evento = json_event
            
            agendamento.save()

        return agendamento


    def atualiza_cliente(self, perfil_id, evento_id):

        qs_agendamento = Agendamento.objects.filter(id=evento_id)
        agendamento = qs_agendamento.first()
        user_perfil_pessoa = PerfilUsuario.objects.filter(id=perfil_id).first()
        agendamento.pessoa = user_perfil_pessoa.usuario
        agendamento.save()


    def atualiza_json(self, id_json_evento, json_evento):
        
        qs_agendamento = Agendamento.objects.filter(id_jsondiv_evento=id_json_evento)
        agendamento = qs_agendamento.first()
        if agendamento is not None:
            if agendamento.json_evento != json_evento:
                agendamento.json_evento = json_evento
                agendamento =  agendamento.save()

        return qs_agendamento
    
    def gera_intervalos(self, hora_inicio, hora_fim, data_evento, profissional):

        hora_inicio = datetime.strptime(f"{data_evento.year}-{data_evento.month}-{data_evento.day} {hora_inicio}", 
                                        "%Y-%m-%d %H:%M")
        hora_fim = datetime.strptime(f"{data_evento.year}-{data_evento.month}-{data_evento.day} {hora_fim}", 
                                     "%Y-%m-%d %H:%M")
        
        if hora_inicio > hora_fim:
            raise ValueError("A hora de início deve ser anterior à hora de fim.")

        intervalos = []
        while hora_inicio < hora_fim:
            if hora_inicio > datetime.now():    
                hasAgendamento = self.get_agendamento_by_time(data_evento=data_evento, 
                                                hora_inicio=hora_inicio, 
                                                hora_final=(hora_inicio + timedelta(minutes=50)),
                                                profissional=profissional) 
                if hasAgendamento:
                    intervalos.append((hora_inicio.strftime('%H:%M'), (hora_inicio + timedelta(minutes=35)).strftime('%H:%M')))
            hora_inicio += timedelta(minutes=35)

        return intervalos    
    
    def create_json_evento(self, title, dia, mes, ano, horario_inicio, horario_fim, id_jsondiv_evento):
       
        data_from = datetime.strptime(f"{ano}-{mes}-{dia} {horario_inicio}", "%Y-%m-%d %H:%M")
        data_to = datetime.strptime(f"{ano}-{mes}-{dia} {horario_fim}", "%Y-%m-%d %H:%M")
        
        data_from_iso = data_from.isoformat().replace('+00:00', '.000Z')
        data_to_iso = data_to.isoformat().replace('+00:00', '.000Z')
        agora = datetime.now(timezone.utc).isoformat()
        dict_json = {
                       "from": data_from_iso,
                       "to": data_to_iso,
                       "title": title,
                       "description": "",
                       "location":"",
                       "group":"",
                       "isAllDay": False,
                       "showAlerts": True,
                       "showAsBusy": True,
                       "color": None,
                       "colorText": None,
                       "colorBorder": None,
                       "repeatEveryExcludeDays": [],
                       "repeatEnds": None,
                       "url": "",
                       "repeatEveryCustomValue": 1,
                       "type": 0,
                       "customTags": None,
                       "alertOffset": 0,
                       "repeatEvery": 0,
                       "repeatEveryCustomType": 0,
                       "id": id_jsondiv_evento,
                       "created": agora,
                    }
        return json.dumps(dict_json)
   
    def gerar_string_aleatoria(self, tamanho=32):
    
        caracteres = string.hexdigits

        # Gera uma string aleatória de caracteres hexadecimais
        random_string = ''.join(random.choice(caracteres) for _ in range(tamanho))
        random_string = random_string.lower() 

        return f"{random_string[:8]}-{random_string[8:12]}-{random_string[12:16]}-{random_string[16:20]}-{random_string[20:]}"
    
    def get_agendamento_by_time(self, data_evento, hora_inicio, hora_final, profissional):
        
        agendamento = Agendamento.objects.filter(
                                            data_evento=data_evento,
                                            profissional=profissional
                                            ).filter(
                                                Q(hora_inicio__gte=hora_inicio.time()) &
                                                Q(hora_inicio__lt=hora_final.time())).first()
        if agendamento is not None:
            return False
        return True
    
    def envia_email(self, user, profissional, data_evento, horario_inicio_fim, request):
        py_email = PyEmail(user.email)
        data_evento = datetime.strptime(data_evento, '%Y-%m-%d')
        data_evento = data_evento.strftime('%d/%m/%Y')
        tp_horario_inicio_fim = eval(horario_inicio_fim)
        horario_inicio = tp_horario_inicio_fim[0]
        horario_fim = tp_horario_inicio_fim[1]
        py_email.set_body(user=user, 
                          profissional=profissional, 
                          data_evento=data_evento, 
                          horario_inicio=horario_inicio,
                          horario_fim=horario_fim, 
                          request=request)
        py_email.enviar()
        
    def envia_sms(self, user, data_evento, agendamento, horario_inicio_fim):
        data_evento = datetime.strptime(data_evento, '%Y-%m-%d')
        data_evento = data_evento.strftime('%d/%m/%Y')
        telefone = PerfilUsuario.objects.get(usuario=user).telefone
        tp_horario_inicio_fim = eval(horario_inicio_fim)
        horario_inicio = tp_horario_inicio_fim[0]    
        horario_fim = tp_horario_inicio_fim[1]

        url = "https://disparo.smsdobrasil.com.br/api/v2/sms/"
        
        mensagem_texto = f'''Ola {user.first_name}, seu agendamento no dia {data_evento}, das {horario_inicio} as {horario_fim}, foi concluido com sucesso.'''

        payload = {
            'sendSmsRequest': {
                'to': telefone,
                'message': mensagem_texto,
                'id': agendamento.id,
                'serviceId': 0,
                'schedule': "",
                'callbackUrl': "",
                'costCenterName': "centro_geral",
                'checkWhitelist': True,
                'checkBlacklist': True,
                'blacklistVars': [],
                'variables': {
                    'token': "string",
                }
            }
        }
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'Authorization': 'Basic UkFGQUVMUkFNT1M6NGc1Qjg0SzRZMkI='
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        print(response.text.encode('utf8'))