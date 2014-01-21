# coding=utf-8
from iampacks.cross.correo.forms import MailForm
from django import forms
from django.utils.translation import ugettext_lazy

class MailProductoraForm(MailForm):
  pass

class MailAgenciadosForm(forms.Form):
  asunto=forms.CharField(widget=forms.TextInput(attrs={'class':'asunto_mail'}))

