from __future__ import annotations
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.models import DjangoJobExecution
from .tasks import send_agendamento_notifications
import logging
import base64

logger = logging.getLogger(__name__)

public_key_base64 = "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEBo2IVqQCPLIRENnN0eJDA1mILELPv6Qo4CLr/KcbnXrFfYVJHKlxHe71JrXy+PZm+IOdLqTg6WKGKqFuizz10g=="
public_key_bytes = base64.b64decode(public_key_base64)
public_key_base64url = base64.urlsafe_b64encode(public_key_bytes).rstrip(b'=').decode('utf-8')

print(public_key_base64url)

def start():
    scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)  
    scheduler.add_job(
        send_agendamento_notifications,
        trigger=CronTrigger(minute="*/10"),
        hour="17",
        minute="12",
        id="send_agendamento_notifications",
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Agendamento da tarefa send_agendamento_notifications")

    try:
        scheduler.start()
    except Exception as e:
        logger.error(f"Erro ao iniciar o agendador: {e}")