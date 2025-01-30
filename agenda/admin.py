from django.contrib import admin
from .models import Agendamento, Configuracao

class AgendamentoAdmin(admin.ModelAdmin):
    display_fields = ['pessoa', 'profissional', 'titulo', 'data_evento', 'hora_inicio', 'hora_final']

class ConfiguracaoAdmin(admin.ModelAdmin):
    display_fields = ['url_atualiza_json', 'tempo_duracao_evento']

admin.site.register(Agendamento, AgendamentoAdmin)
admin.site.register(Configuracao, ConfiguracaoAdmin)