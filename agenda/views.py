from django.shortcuts import render
from django.views import View
from .models import Agendamento

class Principal(View):
    
    def get(self, *args, **kwargs):
        
        context = {
            'agendamentos' : Agendamento.objects.all()
        }

        return render(self.request, 'agenda/agenda.html', context)
    
    
    def post(self, *args, **kwargs):
        
        quantidade = self.request.POST.get('quantidade')
        preco_final = self.request.POST.get('quantidade')
        id_variacao = self.request.POST.get('id_variacao')
        user = self.request.user
        ProdutoService().salvar_entrada_produto(id_variacao, preco_final, quantidade, user)

        return redirect('produto:tabela')

