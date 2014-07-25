# -*- encoding: utf-8 -*-

from django.db import models

from utils.models import EditorialModel, BaseManager


class Loja(EditorialModel):
    nome = models.CharField(u'Nome', max_length=100, null=True, blank=False)
    logo = models.CharField(u'Logo', max_length=100, null=True, blank=True)
    telefone = models.CharField(u'telefone', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name=u'Loja'
        verbose_name_plural=u'Lojas'
        ordering = ['nome']

    def __unicode__(self):
        return u'%s' % self.nome