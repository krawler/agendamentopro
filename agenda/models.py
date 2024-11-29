from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Agendamento(models.Model):
    pessoa = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_pessoa')
    profissional = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_profissional')
    data_evento = models.DateField(default=datetime.now().date())
    hora_inicio = models.TimeField(default=timezone.now().time())
    hora_final = models.TimeField(default=timezone.now().time())
    observacao = models.TextField(max_length=500, null=True)
    desativado = models.BooleanField(default=False)
