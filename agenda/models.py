from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Agendamento(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    profissional = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    data = models.DateField(default=datetime.now().date())
    hora_inicio = models.TimeField(default=timezone.now().time())
    hora_final = models.TimeField(default=timezone.now().time())
    observacao = models.TextField(max_length=500)
    desativado = models.BooleanField(default=False)
