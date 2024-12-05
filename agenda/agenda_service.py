from .models import Agendamento
from datetime import datetime

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
            if agendamento.json_evento == json_evento:
                return '{return false}'
            else:
                agendamento.json_evento = json_evento
                agendamento =  agendamento.save()
            
            return agendamento
        
        