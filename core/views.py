from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify
from django.core.mail import EmailMessage

from weasyprint import HTML

from core.models import Questionario, Pergunta
from core.forms import EmailForm


def home(request):
    questionarios = Questionario.objects.filter(pergunta__isnull=False).distinct()
    context = {'questionarios': questionarios}
    return render(request, 'core/listagem_questionario.html', context)


def detalhes_questionario(request, id):
    questionario = Questionario.objects.get(id=id)
    perguntas = Pergunta.objects.filter(questionario=questionario).distinct()
    form = EmailForm()
    context = {
        'questionario': questionario,
        'perguntas': perguntas,
        'formulario': form
    }
    return render(request, 'core/detalhes_questionario.html', context)


def envio_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            id_questionario = int(request.POST.get('questionario'))
            destinatario = request.POST.get('email')
            questionario = Questionario.objects.get(id=id_questionario)
            titulo_formatado = slugify(questionario.titulo)
            envia_pdf(request, id_questionario, destinatario)
            return HttpResponseRedirect('/')


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
    with fs.open('detalhes-{}.pdf'.format(titulo_formatado)) as pdf:
        arquivo = pdf.read()
        response = HttpResponse(arquivo, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="detalhes-{}.pdf"'.format(titulo_formatado)

    return response


def envia_pdf(request, id, destinatario):
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
    html.write_pdf(target='detalhes-{}.pdf'.format(titulo_formatado))

    fs = FileSystemStorage('/tmp')
    with fs.open('detalhes-{}.pdf'.format(titulo_formatado)) as pdf:
        arquivo = pdf.read()
        response = HttpResponse(arquivo, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="detalhes-{}.pdf"'.format(titulo_formatado)
        email = EmailMessage(
            subject=f'Detalhes { questionario.titulo }',
            body=f'Email enviado com o relatório do { questionario.titulo } anexo',
            to=[destinatario],
        )
        email.attach_file('/tmp/detalhes-{}.pdf'.format(titulo_formatado))
        email.send()
