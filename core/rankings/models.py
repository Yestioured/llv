# -*- encoding: utf-8 -*-
from django.db import models

from utils.models import BaseModel
from lojas.models import Loja

class Intervalo(BaseModel):
    inicio = models.DateField(u'Início', null=False, blank=False)
    fim = models.DateField(u'Fim', null=False, blank=False)

    class Meta:
        verbose_name = u'Intervalo'
        verbose_name_plural = u'Intervalos'


class Ponto(BaseModel):
    intervalo = models.ForeignKey(Intervalo, verbose_name='Intervalo', related_name='pontos')
    loja = models.ForeignKey(Loja, verbose_name='Loja', related_name='pontos')
    produtos = models.IntegerField(u'Produtos')  # 1 ponto cada
    fotos = models.IntegerField(u'Fotos')  # 1 ponto cada
    likes = models.IntegerField(u'Curtidas')  # 1 ponto cada
    shares = models.IntegerField(u'Compartilhadas')  # 2 pontos cada
    desconto_30 = models.IntegerField(u'Descontos até 30%') # 1 ponto cada
    desconto_50 = models.IntegerField(u'Descontos de 31% a 50%') # 2 pontos cada
    desconto_70 = models.IntegerField(u'Descontos de 51% a 70%') # 3 pontos cada
    desconto_100 = models.IntegerField(u'Descontos acima de 70%') # 4 pontos cada

    class Meta:
        verbose_name = u'Ponto'
        verbose_name_plural = u'Pontos'

    def __unicode__(self):
        return u'pontos do intervalo %s da loja %s' % (self.intervalo, self.loja)
