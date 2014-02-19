# coding=utf-8
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from iampacks.agencia.agencia.models import Agenciado, DireccionAgenciado, Telefono, FotoAgenciado, VideoAgenciado
from datetime import date
from django.contrib import messages
from iampacks.agencia.trabajo.models import Postulacion, Rol
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from iampacks.agencia.agenciado.forms import *

def get_agenciado(request):
  try:
    agenciado=Agenciado.objects.get(user__id=request.user.id)
  except Agenciado.DoesNotExist:
    agenciado=Agenciado(
      user=request.user,
      nombre = request.user.first_name,
      apellido = request.user.last_name,
      mail = request.user.email,
      fecha_ingreso = date.today(),
      activo=False,
    )

  return agenciado

@login_required
def index(request):
  agenciado = get_agenciado(request)

  if request.method == 'POST':
    form = AgenciadoForm(request.POST,instance=agenciado)
    direccionFormSet = DireccionFormSet(request.POST,request.FILES,instance=agenciado)
    telefonoFormSet=TelefonoFormSet(request.POST,request.FILES,instance=agenciado)
    fotoAgenciadoFormSet=FotoAgenciadoFormSet(request.POST,request.FILES,instance=agenciado)
    videoAgenciadoFormSet=VideoAgenciadoFormSet(request.POST,request.FILES,instance=agenciado)
    if form.is_valid() and direccionFormSet.is_valid() and telefonoFormSet.is_valid() and fotoAgenciadoFormSet.is_valid() and videoAgenciadoFormSet.is_valid():
      form.save()
      direccionFormSet.save()
      telefonoFormSet.save()
      fotoAgenciadoFormSet.save()
      videoAgenciadoFormSet.save()
      messages.success(request, _(u'Dados atualizados com sucesso'))
      next_page = form.cleaned_data['next_page']
      if not next_page:
        next_page = '/agenciado/'
      return redirect(next_page)
  else:
    next_page = request.GET.get('next')
    form = AgenciadoForm(instance=agenciado,initial={'next_page':next_page})
    direccionFormSet = DireccionFormSet(instance=agenciado)
    telefonoFormSet=TelefonoFormSet(instance=agenciado)
    fotoAgenciadoFormSet=FotoAgenciadoFormSet(instance=agenciado)
    videoAgenciadoFormSet=VideoAgenciadoFormSet(instance=agenciado)
  return render(request,'agenciado/agenciado.html',{'form':form, 'direccionFormSet':direccionFormSet, 'telefonoFormSet':telefonoFormSet, 'fotoAgenciadoFormSet':fotoAgenciadoFormSet, 'videoAgenciadoFormSet':videoAgenciadoFormSet, })

@login_required
def postular(request):
  # Se obtiene el rol de la postulación
  rol_id = request.GET.get('rol_id')
  try:
    rol = Rol.objects.get(pk=rol_id,trabajo__publicado=True)
  except Rol.DoesNotExist:
    messages.error(request,_(u'O perfil do trabalho para o qual quer aplicar nao foi encontrado'))
    return redirect('/trabajo/busquedas/')
  # Se verifica que el usuario tenga cargado su perfil
  try:
    request.user.agenciado
  except Agenciado.DoesNotExist:
    messages.info(request,
      _(u'Para aplicar ao perfil %(rol)s do trabalho <a href=%(url)s>%(trabajo)s</a> tem que completar seus dados de Agenciado')%{
        'rol':rol.descripcion,'url':'/trabajo/busquedas/?id=%s'%rol.trabajo.id,'trabajo':rol.trabajo.titulo})
    return redirect('/agenciado/?next=%s'%request.get_full_path())
  # Se realiza la postulación
  try:
    postulacion=Postulacion.objects.get(agenciado=request.user.agenciado,rol=rol)
  except Postulacion.DoesNotExist:
    postulacion=Postulacion(agenciado=request.user.agenciado,rol=rol,estado='PA')
    postulacion.save()

  messages.success(request,_(u'Aplicação para o perfil "%s" realizada com sucesso.')%rol.descripcion)
  messages.info(request,_(u'A aplicação vai ser analizada por nosso equipe, muito obrigado por sua postulação.'))
  return redirect('/trabajo/busquedas/?id=%s'%rol.trabajo.id)

from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView as DjangoSessionWizardView
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

class SessionWizardView(DjangoSessionWizardView):
  def get_form(self, step=None, data=None, files=None):
    """
    Constructs the form for a given `step`. If no `step` is defined, the
    current step will be determined automatically.
    The form will be initialized using the `data` argument to prefill the
    new form. If needed, instance or queryset (for `ModelForm` or
    `ModelFormSet`) will be added too.
    """
    if step is None:
        step = self.steps.current
    # prepare the kwargs for the form instance.
    kwargs = self.get_form_kwargs(step)
    kwargs.update({
        'data': data,
        'files': files,
        'prefix': self.get_form_prefix(step, self.form_list[step]),
        'initial': self.get_form_initial(step),
    })
    if issubclass(self.form_list[step], forms.ModelForm):
        # If the form is based on ModelForm, add instance if available
        # and not previously set.
        kwargs.setdefault('instance', self.get_form_instance(step))
    elif issubclass(self.form_list[step], forms.models.BaseModelFormSet):
        # If the form is based on ModelFormSet, add queryset if available
        # and not previous set.
        kwargs.setdefault('instance', self.get_form_instance(step))
    return self.form_list[step](**kwargs)

class AgenciadoWizard(SessionWizardView):

  form_list = [
    AgenciadoDatosPersonalesForm, 
    AgenciadoCaracteristicasForm,
    AgenciadoHabilidadesForm,
    DireccionFormSet, 
    TelefonoFormSet, 
    FotoAgenciadoFormSet,
    VideoAgenciadoFormSet,
    AgenciadoOtrosDatosForm,
    ]
  template_name = 'agenciado/wizard.html'
  file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'tmp'))
  instance = None

  def done(self, form_list, **kwargs):
    formsets = []
    cleaned_data = {}
    for form in form_list:
      if isinstance(form, forms.models.BaseModelFormSet):
        formsets.append(form)
      else:
        self.instance.__dict__ = dict(self.instance.__dict__.items()+form.cleaned_data.items())
    self.instance.save()
    for formset in formsets:
      formset.save()
    messages.success(self.request, _(u'Dados atualizados com sucesso'))
    return HttpResponseRedirect('/agenciado/wizard/')

  def get_form_instance(self, step):
    if not self.instance:
      self.instance = get_agenciado(self.request)
    return self.instance
