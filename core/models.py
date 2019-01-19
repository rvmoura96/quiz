from django.db import models


class Questionario(models.Model):
    titulo = models.CharField('Titulo', max_length=255)
    numero_de_respotas = models.PositiveIntegerField(default=0)


class Pergunta(models.Model):
    pergunta = models.CharField('Pergunta', max_length=255)
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)


class Resposta(models.Model):
    resposta = models.CharField('Resposta', max_length=255)
    correta = models.BooleanField(default=False)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
