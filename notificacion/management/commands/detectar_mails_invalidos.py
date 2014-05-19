# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User
from iampacks.agencia.notificacion.models import NotificacionCuentaAgenciadoExistente
import imaplib
import re

RE_MAIL_INVALIDO = [
  re.compile('action not taken: mailbox unavailable'),
  re.compile('Host or domain name not found'),
  re.compile('The email account that you tried to reach does not exist'),
  re.compile('Message.*received.'),
  re.compile('User unknown'),
  re.compile('Recipient address rejected'),
  re.compile("delivery error: dd This user doesn't have"),
  ]

RE_INVALID_MAIL = re.compile('%s\r\nTo: ([^ ]+@[^ \r\n]+)'%settings.AMBIENTE.email.user)

class MailNoInvalido(Exception):
  pass

class DireccionEmailNoEncontrada(Exception):
  pass

class Command(BaseCommand):

  help=_(u'Detecta mails invalidos a partir de respuestas automáticas de servidores de mail.')

  def get_mail_invalido(self, data):

    es_invalido = False

    for regexp in RE_MAIL_INVALIDO:
      if regexp.match(data):
        es_invalido = True
        break

    if not es_invalido:
      raise MailNoInvalido()

    match = RE_INVALID_MAIL.find(data)

    if match:
      return match.group(1)

    raise DireccionEmailNoEncontrada()


  def handle(self,*args,**options):

    imap = imaplib.IMAP4('localhost')
    imap.login(settings.AMBIENTE.email.user,settings.AMBIENTE.email.password)
    imap.select('inbox')
    
    result, data = imap.uid('search', None, 'ALL')

    uids = data[0].split(' ')

    for uid in uids:
      self.stdout.write('Se procesa mensaje %s\n'%uid)
      result, data = imap.uid('fetch', uid, '(RFC822)')

      try:
        email = self.get_mail_invalido(data[0][1])
        self.stdout.write('%s\n'%email)
      except MailNoInvalido:
        pass

