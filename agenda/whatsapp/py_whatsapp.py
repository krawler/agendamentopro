from twilio.rest import Client
from django.conf import settings

def enviar_mensagem_whatsapp(numero_cliente, mensagem):
    """
    Envia uma mensagem para o WhatsApp de um cliente.

    Args:
        numero_cliente (str): Número de telefone do cliente com o código do país (ex: +5511999999999).
        mensagem (str): Mensagem a ser enviada.
    """

    # Credenciais da API Twilio
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            from_=settings.TWILIO_PHONE_NUMBER,  # Seu número do WhatsApp Business
            body=mensagem,
            to=numero_cliente  # Formato para o WhatsApp
        )
        print(f"Mensagem enviada com sucesso para {numero_cliente}! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"Erro ao enviar mensagem para {numero_cliente}: {e}")
        return False