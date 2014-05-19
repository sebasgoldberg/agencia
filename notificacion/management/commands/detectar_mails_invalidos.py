# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User
from iampacks.agencia.notificacion.models import NotificacionCuentaAgenciadoExistente, MailInvalido
import imaplib
import re

RE_MAIL_INVALIDO = [
  'action not taken: mailbox unavailable',
  'Host or domain name not found',
  'The email account that you tried to reach does not exist',
  'Message.*received.',
  'User unknown',
  'Recipient address rejected',
  "delivery error: dd This user doesn't have",
  ]

RE_DIRECCION_MAIL_INVALIDO = re.compile('%s\r\nTo: ([^ ]+@[^ \r\n]+)'%settings.AMBIENTE.email.user)

class MailNoInvalido(Exception):
  pass

class DireccionEmailNoEncontrada(Exception):
  pass

class Command(BaseCommand):

  help=_(u'Detecta mails invalidos a partir de respuestas automáticas de servidores de mail.')

  option_list = BaseCommand.option_list + (
    make_option('--silencioso',default=False),
    )

  def get_mail_invalido(self, data):

    es_invalido = False

    for regexp in RE_MAIL_INVALIDO:
      if re.search(regexp,data):
        es_invalido = True
        break

    if not es_invalido:
      raise MailNoInvalido()

    match = re.search(RE_DIRECCION_MAIL_INVALIDO,data)

    if match:
      return match.group(1)

    if not self.silencioso:
      print data
      raise DireccionEmailNoEncontrada()

  def handle(self,*args,**options):

    self.silencioso = options['silencioso']

    imap = imaplib.IMAP4('localhost')
    imap.login(settings.AMBIENTE.email.user,settings.AMBIENTE.email.password)
    imap.select('inbox')
    
    result, data = imap.uid('search', None, 'ALL')

    uids = data[0].split(' ')

    for uid in uids:
      result, data = imap.uid('fetch', uid, '(RFC822)')

      try:
        email = self.get_mail_invalido(data[0][1])
        if email is not None:
          mail_invalido = MailInvalido.objects.get_or_create(email=email)
      except MailNoInvalido:
        pass

