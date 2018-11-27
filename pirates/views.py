from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField
from django.http import HttpResponseRedirect
from django.views import View
from django.forms import ModelForm
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView

from .models import Tesouro
# Create your views here.
class ListarTesouros(ListView):
    model = Tesouro
    template_name = 'lista_tesouros.html'

    def get_queryset(self):
        return Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                            output_field=DecimalField(max_digits=10,\
                                                    decimal_places=2,\
                                                     blank=True)\
                                                    ))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_geral'] = 0
        for tesouro in context['object_list']:
            context['total_geral'] += tesouro.valor_total
        return context

class RemoverTesouro(DeleteView):
    model = Tesouro
    fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
    template_name = 'salvar_tesouro.html'
    success_url = reverse_lazy('lista_tesouros')

class InserirTesouro(CreateView):
	model = Tesouro
	fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
	template_name = 'salvar_tesouro.html'
	success_url = reverse_lazy('lista_tesouros')

class AtualizarTesouro(UpdateView):
    model = Tesouro
    fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
    template_name = 'salvar_tesouro.html'
    success_url = reverse_lazy('lista_tesouros')

