# -*- encoding: utf-8 -*-

from django.db import models

from utils.models import BaseModel, EditorialModel
from utils.custom_email import TemplatedEmail
from lojas.models import Loja


class BaseNotificacao(EditorialModel):
    mensagem = models.CharField(u'Mensagem', null=True, blank=True,
                                max_length=255)
    lida = models.BooleanField(u'Lida?', default=False)

    class Meta:
        abstract = True
        verbose_name = u'Base da Notificação'
        verbose_name_plural = u'Base das Notificações'
        ordering = ('-data_criacao',)


class Notificacao(BaseNotificacao):
    resolvida = models.BooleanField(u'Resolvida?', default=False)
    oferta = models.ForeignKey('geral.Oferta', verbose_name=u'Oferta',
                               null=True,
                               related_name='notificacoes', blank=True)
    solicitante = models.ForeignKey('geral.Perfil', verbose_name=u'Autor',
                                    blank=True, null=True,
                                    related_name='solicitante')
    responsavel = models.ForeignKey('geral.Perfil', null=True, blank=False,
                                    verbose_name=u'Marketing responsável',
                                    related_name='responsavel')
    enviada_mkt = models.BooleanField(u'Enviada para o marketing?',
                                      default=False)
    enviada_lojista = models.BooleanField(u'Enviada para o lojista?',
                                          default=False)

    class Meta:
        verbose_name = u'Notificação'
        verbose_name_plural = u'Notificações'

    def __unicode__(self):
        return u'%s' % self.oferta

    def save(self, *args, **kwargs):
        if not self.mensagem:
            self.mensagem = u'Nova oferta para aprovacao - %s' % self.oferta
        super(Notificacao, self).save(*args, **kwargs)

    def notifica_criacao(self):
        if self.responsavel and self.responsavel.user.email:
            try:
                TemplatedEmail([self.responsavel.user.email], self.mensagem,
                               'email/notificacao.html',self.to_dict(),send_now=True)
                self.enviada_mkt = True
                self.save()
            except:
                raise

    def notifica_aprovacao(self):
        autor = self.solicitante
        if autor and autor.user.email:
            assunto = u'Sua oferta foi aprovada e publicada'
            try:
                TemplatedEmail([autor.user.email], assunto,
                               'email/aprovacao.html', self.to_dict(),
                               send_now=True)
                self.enviada_lojista = True
                self.resolvida = True
                self.lida = True
                self.save()
            except:
                raise

    def to_dict(self):
        return {'id': self.id,
                'mensagem': self.mensagem,
                'oferta': self.oferta,
                'lojista': self.solicitante}



class Solicitacao(BaseNotificacao):
    MENSAGEM_DEFAULT = u'As pessoas estão buscando ofertas da sua loja.'

    nome = models.CharField(u'Nome', null=True, blank=False, max_length=250)
    email = models.CharField(u'E-mail', null=True, blank=False, max_length=250)
    loja = models.ForeignKey(Loja, verbose_name=u'Loja', null=True,
                             blank=True, related_name='solicitacoes')

    class Meta:
        verbose_name = u'Solicitação de Loja'
        verbose_name_plural = u'Solicitações de Lojas'

    def __unicode__(self):
        return u'%s (%s) - %s' % (self.nome, self.email, self.loja)

    def save(self, *args, **kwargs):
        if not self.mensagem:
            self.mensagem = self.MENSAGEM_DEFAULT
        super(Solicitacao, self).save(*args, **kwargs)