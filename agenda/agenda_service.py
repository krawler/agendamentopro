from .models import Agendamento
from datetime import datetime

class Agenda_Service():

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Agenda_Service, cls).__new__(cls)
        return cls.instance    

    def adiciona_evento(self, dt_inicio, dt_final, data_evento, profissional, json_event):
        
        data_evento = datetime.strptime(data_evento, '%Y-%m-%d')
        hora_inicio = datetime.strptime(dt_inicio, '%H:%M:%S')
        hora_final = datetime.strptime(dt_final, '%H:%M:%S')

        agenda = Agendamento(pessoa=None,
                            profissional=profissional, 
                            data_evento=data_evento, 
                            hora_inicio=hora_inicio, 
                            hora_final=hora_final,
                            json_evento=json_event)
        agenda.save()

        return agenda
