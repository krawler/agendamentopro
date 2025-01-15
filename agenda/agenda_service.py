import json
import random
import string
from .models import Agendamento
from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import User

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

    def adiciona_evento_formulario(self, hora_inicio_fim, data_evento, usuario):
           
        profissional = User.objects.filter(is_staff=True).first()
        
        id_jsondiv_evento = self.gerar_string_aleatoria()
        
        data_evento = datetime.strptime(data_evento, '%Y-%m-%d')
        tupla_horarios = eval(hora_inicio_fim)
        horario_inicio = tupla_horarios[0]
        horario_fim = tupla_horarios[1]
        
        json_event = self.create_json_evento(None,  
                                             data_evento.day,                                       
                                             data_evento.month,                                              
                                             data_evento.year, 
                                             horario_inicio, 
                                             horario_fim, 
                                             id_jsondiv_evento)
        json_event = str(json_event).replace('"', '\\"').replace(' ', '')        
        datetime_hora_inicio = data_evento.strptime(horario_inicio, '%H:%M')
        datetime_horario_fim = data_evento.strptime(horario_fim, '%H:%M')
        agenda = Agendamento(pessoa=usuario,
                             profissional=profissional, 
                             data_evento=data_evento, 
                             hora_inicio=datetime_hora_inicio, 
                             hora_final=datetime_horario_fim,
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
    
    def gera_intervalos(self, hora_inicio, hora_fim):

        # Converter as horas de string para objetos datetime
        inicio = datetime.strptime(hora_inicio, '%H:%M')
        fim = datetime.strptime(hora_fim, '%H:%M')

        # Verificar se a hora de início é anterior à hora de fim
        if inicio > fim:
            raise ValueError("A hora de início deve ser anterior à hora de fim.")

        intervalos = []
        while inicio < fim:
            # Adicionar o intervalo à lista
            intervalos.append((inicio.strftime('%H:%M'), (inicio + timedelta(minutes=50)).strftime('%H:%M')))
            # Avançar 50 minutos
            inicio += timedelta(minutes=50)

        return intervalos    
    
    def create_json_evento(self, title, dia, mes, ano, horario_inicio, horario_fim, id_jsondiv_evento):
        hora_inicio = horario_inicio.split(':')[0]
        minuto_inicio = horario_inicio.split(':')[1]
        hora_fim = horario_fim.split(':')[0]
        minuto_fim = horario_fim.split(':')[1]
        data_from = datetime(ano, mes, dia, int(hora_inicio), int(minuto_inicio), 0, 0, timezone.utc)
        data_to = datetime(ano, mes, dia, int(hora_fim), int(minuto_fim), 0, 0, timezone.utc)
        data_from_iso = data_from.isoformat().replace('+00:00', '.000Z')
        data_to_iso = data_to.isoformat().replace('+00:00', '.000Z')
        agora = datetime.now(timezone.utc).isoformat()
        dict_json = {
                       "from": data_from_iso,
                       "to": data_to_iso,
                       "title":"* Novo evento criado no formulario",
                       "description":"",
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

        # Insere os hifens nos locais corretos
        return f"{random_string[:8]}-{random_string[8:12]}-{random_string[12:16]}-{random_string[16:20]}-{random_string[20:]}"
        