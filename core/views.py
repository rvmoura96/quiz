from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify

from weasyprint import HTML

from core.models import Questionario, Pergunta


def home(request):
    questionarios = Questionario.objects.filter(pergunta__isnull=False).distinct()
    context = {'questionarios': questionarios}
    return render(request, 'core/listagem_questionario.html', context)


def detalhes_questionario(request, id):
    questionario = Questionario.objects.get(id=id)
    perguntas = Pergunta.objects.filter(questionario=questionario).distinct()
    context = {
        'questionario': questionario,
        'perguntas': perguntas,
    }
    return render(request, 'core/detalhes_questionario.html', context)


def detalhes_em_pdf(request, id):
    questionario = Questionario.objects.get(id=id)
    titulo = questionario.titulo
    titulo_formatado = slugify(titulo)
    perguntas = Pergunta.objects.filter(questionario=questionario).distinct()
    context = {
        'questionario': questionario,
        'perguntas': perguntas,
    }
    html_string = render_to_string('core/template_pdf.html', context)
    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/detalhes-{}.pdf'.format(titulo_formatado))

    fs = FileSystemStorage('/tmp')
    with fs.open(f'mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="detalhes-{}.pdf"'.format(titulo_formatado)
        return response

    return response
