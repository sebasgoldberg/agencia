# coding=utf-8
# Create your views here.

from django.shortcuts import render, redirect
from iampacks.agencia.trabajo.models import Trabajo, ItemPortfolio
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from iampacks.cross.usuario.signals import usuario_after_register_before_redirect 
from django.conf import settings

def notify_register(sender,request,**kwargs):
  messages.info(request,_(u'Por favor atualize os dados do seu perfil a ser analizado por nossa agencia.'))

usuario_after_register_before_redirect.connect(notify_register)

def index(request):
  if settings.AMBIENTE.sitio.externo.url:
    return redirect(settings.AMBIENTE.sitio.externo.url)
  trabajos = Trabajo.objects.filter(publicado=True).order_by('-fecha_ingreso')[:3]
  portfolio = ItemPortfolio.objects.order_by('-fecha')[:3]
  return render(request,'agencia/index.html', { 'trabajos': trabajos, 'portfolio': portfolio})

def contacto(request):
  return render(request,'agencia/contacto.html')

