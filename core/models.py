from django.db import models
from django.db.models import Max

class Questionario(models.Model):
    titulo = models.CharField('Titulo', max_length=255)
    numero_de_respotas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo


class Pergunta(models.Model):
    pergunta = models.CharField('Pergunta', max_length=255)
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)

    def mais_escolhida(self):
        resposta = Resposta.objects.filter(
            pergunta=self
            ).latest('vezes_selecionada')

        return resposta

    def respostas(self):
        """Restorna as repostas atreladas a esta pergunta."""
        return Resposta.objects.filter(pergunta=self).distinct()

    def lista_das_respostas(self):
        """Retorna uma lista contendo o valor de cada resposta.

        Retorna uma lista contendo o valor de cada resposta relacionada a
        pergunta instanciada.
        """
        respostas = Resposta.objects.filter(pergunta=self).distinct()
        lista_das_respostas = [
            resposta.resposta for resposta in respostas
        ]

        return lista_das_respostas

    def contagem_das_respostas(self):
        """Retorna uma lista contendo o número de vezes de cada resposta.

        Retorna uma lista contendo o valor do número de vezes que cada resposta
        foi selecionada pergunta instanciada.
        """
        respostas = Resposta.objects.filter(pergunta=self).distinct()
        lista_das_contagens = [
            resposta.vezes_selecionada for resposta in respostas
        ]

        return lista_das_contagens

    def clean(self):
        """Valida o número máximo de perguntas relacionadas a um questionarios.

        Caso o questionario utilizado no relacionamento, tenha um total de
        perguntas relacionadas a ele >= 10, a instância de pergunta em questão
        não será salva.
        """
        if self.questionario.pergunta_set.exclude(pk=self.pk).count() >= 10:
            raise Exception(
                f'{self.questionario} possuí o limite de 10 perguntas.'
            )

    def __str__(self):
        return self.pergunta


class Resposta(models.Model):
    resposta = models.CharField('Resposta', max_length=255)
    correta = models.BooleanField(default=False)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    vezes_selecionada = models.PositiveIntegerField(default=0)

    def clean(self):
        """Valida o número máximo de respostas relacionadas a uma pergunta.

        Caso a pergunta utilizada no relacionamento, tenha um total de
        respostas relacionadas a ele >= 4, a instância de resposta em questão
        não será salva.
        """
        if self.pergunta.resposta_set.exclude(pk=self.pk).count() >= 4:
            raise Exception(
                f'{self.pergunta} possuí o limite de 4 opções.'
            )

    def __str__(self):
        return self.resposta


class Email(models.Model):
    email = models.EmailField()
