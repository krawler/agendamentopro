'''
from twilio.rest import Client
from django.conf import settings
from agenda.models import Configuracao

def enviar_mensagem_whatsapp(numero_cliente, mensagem):
    """
    Envia uma mensagem para o WhatsApp de um cliente.

    Args:
        numero_cliente (str): Número de telefone do cliente com o código do país (ex: +5511999999999).
        mensagem (str): Mensagem a ser enviada.
    """

    # Credenciais da API Twilio
    config = Configuracao.objects.first() 
    account_sid = config.twilio_account_sid  # twilio_account_sid
    auth_token = config.twilio_auth_token  # twilio_auth_token


    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_=config.twilio_phone_number,  # Seu número do WhatsApp Business
            body=mensagem,
            to=numero_cliente  # Formato para o WhatsApp
        )
        print(f"Mensagem enviada com sucesso para {numero_cliente}! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Erro ao enviar mensagem para {numero_cliente}: {e}")
        return False
'''    