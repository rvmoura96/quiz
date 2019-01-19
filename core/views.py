from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from core.models import Questionario, Pergunta


def home(request):
    questionarios = Questionario.objects.filter(
        pergunta__isnull=False
    ).distinct()

    return render(
        request,
        'core/listagem_questionario.html',
        {'questionarios': questionarios}
    )


def detalhes_questionario(request, id):
    questionario = Questionario.objects.get(id=id)
    perguntas = Pergunta.objects.filter(questionario=questionario).distinct()
    return render(request, 'core/detalhes_questionario.html', {
        'questionario': questionario,
        'perguntas': perguntas,
    })
