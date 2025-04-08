from io import StringIO
import logging
import json
from pathlib import Path
from django_tasks import task
import requests
from webpush import WebPush, WebPushSubscription
from datetime import date, datetime, timedelta, timezone
from django.conf import settings
from perfil.models import  PushSubscription
from .models import Agendamento, Configuracao

logger = logging.getLogger(__name__)

def send_agendamento_notifications():
    logger.info("Sending agendamento notifications...")
    one_day_before = datetime.now().date() + timedelta(days=1)
    agendamentos = Agendamento.objects.filter(data_evento=one_day_before)
    for agendamento in agendamentos:
        message = f"Seu agendamento para atendimento é amanhã!"
        subscription = PushSubscription.objects.get(user=agendamento.pessoa)
        enviar_notificacao(subscription, message)
        logger.info("enviado a notificacao")


def enviar_notificacao(subscription, mensagem):
    try:
        payload = {"head": "Agendamento", "body": mensagem}
        
        logger.info("enviando  a notificacao")
            
        wp = WebPush(private_key=Path("./private_key.pem"), public_key=Path("./public_key.pem"), subscriber=settings.VAPID_SUBJECT)
        
        data = json.dumps(payload)
  
        subscription = WebPushSubscription.model_validate({
           "endpoint": subscription.endpoint,
                "keys": {
                    "p256dh": subscription.p256dh,
                    "auth": subscription.auth,
                },
        })
        
        message = wp.get(message=data, subscription=subscription)
        
        requests.post(subscription.endpoint, data=message.encrypted, headers=message.headers)

        return True

    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")
        return False