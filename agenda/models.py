from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


class Agendamento(models.Model):
    pessoa = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_pessoa')
    profissional = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='user_profissional')
    titulo = models.TextField(max_length=50)
    data_evento = models.DateField(default=datetime.now().date())
    hora_inicio = models.TimeField(default=timezone.now().time())
    hora_final = models.TimeField(default=timezone.now().time())
    observacao = models.TextField(max_length=500, null=True)
    desativado = models.BooleanField(default=False)
    json_evento = models.TextField(max_length=1000)
    id_jsondiv_evento = models.CharField(max_length=60) 
    
    def __str__(self):
        data_evento = self.data_evento.strftime('%d/%m/%Y')
        return f'{data_evento} - {self.hora_inicio} - {self.hora_final}' 


class Configuracao(models.Model):
    url_atualiza_json = models.CharField(max_length=100)
    tempo_duracao_evento = models.IntegerField()
    twilio_account_sid = models.CharField(max_length=100, null=True)
    twilio_auth_token = models.CharField(max_length=100, null=True)
    twilio_phone_number = models.CharField(max_length=100, null=True)
    url_base = models.CharField(max_length=100, null=True)
    email_host = models.CharField(max_length=100, null=True)
    email_smtp = models.CharField(max_length=100, null=True)
    email_port = models.CharField(max_length=100, null=True)
    email_host_password = models.TextField(max_length=100, null=True)
    
    def __str__(self):
        return 'configuração padrão'


class MensagemFila(models.Model):
    agendamento = models.ForeignKey(Agendamento, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_mensagem')
    profissional = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, related_name='agendamento_profissional')
    mensagem = models.TextField(max_length=500, null=False)
    telefone = models.CharField(max_length=15, null=False)
    telefone_profissional = models.CharField(max_length=15, null=False)
    desativado = models.BooleanField(default=False)
    
    class Meta:
        managed = False