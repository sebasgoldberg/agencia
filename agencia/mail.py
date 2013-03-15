# coding=utf-8
from iamsoft.cross.correo.mail import Mail
from iamsoft.agencia.agencia.models import Agencia
from django.utils.translation import ugettext_lazy

class MailAgencia(Mail):

  def actualizar_asunto(self,asunto):
    agencia = Agencia.get_activa()
    return ugettext_lazy(u'%(nombre)s - %(asunto)s') % {'nombre':agencia.nombre, 'asunto':asunto}

  def get_reply_to(self):
    agencia = Agencia.get_activa()
    return agencia.email

