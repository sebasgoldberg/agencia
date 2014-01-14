# coding=utf-8
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from iampacks.agencia.agencia.models import Agenciado, DireccionAgenciado, Telefono, FotoAgenciado, VideoAgenciado
from iampacks.agencia.agencia.models import validarDireccionIngresada, validarTelefonoIngresado, validarFotoIngresada
from datetime import date
from django.forms.models import inlineformset_factory
from django.contrib import messages
from django import forms
from itertools import chain
from django.forms.widgets import CheckboxSelectMultiple, CheckboxInput, HiddenInput
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from iampacks.agencia.trabajo.models import Postulacion, Rol
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from iampacks.agencia.agencia.forms import DireccionAgenciadoFormRelated

class BPCheckboxSelectMultiple(CheckboxSelectMultiple):

  def render(self, name, value, attrs=None, choices=()):
    if value is None: value = []
    has_id = attrs and 'id' in attrs
    final_attrs = self.build_attrs(attrs, name=name)
    output = [u'<div class="row">']
    # Normalize to strings
    str_values = set([force_unicode(v) for v in value])
    for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
      # If an ID attribute was given, add a numeric index as a suffix,
      # so that the checkboxes don't all have the same ID attribute.
      if has_id:
        final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
        label_for = u' for="%s"' % final_attrs['id']
      else:
        label_for = ''

      cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
      option_value = force_unicode(option_value)
      rendered_cb = cb.render(name, option_value)
      option_label = conditional_escape(force_unicode(option_label))
      output.append(u'<div class="span2"><label%s>%s %s</label></div>' % (label_for, rendered_cb, option_label))
      ultimo_fila=(((i+1) % 6) == 0)
      if ultimo_fila:
        output.append(u'</div>')
        output.append(u'<div class="row">')
    # Normalize to strings
    output.append(u'</div>')
    return mark_safe(u'\n'.join(output))

class AgenciadoForm(ModelForm):
  next_page = forms.CharField(widget=forms.HiddenInput,required=False)
  
  class Meta:
    model = Agenciado
    exclude = ('activo', 'fecha_ingreso')
    widgets = {
      'fecha_nacimiento': SelectDateWidget(years=range(date.today().year-100,date.today().year+1)),
      'deportes': BPCheckboxSelectMultiple,
      'danzas': BPCheckboxSelectMultiple,
      'instrumentos': BPCheckboxSelectMultiple,
      'idiomas': BPCheckboxSelectMultiple,
      }

BaseDireccionFormSet = inlineformset_factory(Agenciado, DireccionAgenciado, extra=1, max_num=1, can_delete=False, form = DireccionAgenciadoFormRelated)
BaseTelefonoFormSet = inlineformset_factory(Agenciado, Telefono, extra=6, max_num=6)
BaseFotoAgenciadoFormSet = inlineformset_factory(Agenciado, FotoAgenciado, extra=6, max_num=6)
VideoAgenciadoFormSet = inlineformset_factory(Agenciado, VideoAgenciado, extra=6, max_num=6, exclude=['codigo_video'])

class DireccionFormSet(BaseDireccionFormSet):
  def clean(self):
    super(DireccionFormSet,self).clean()
    validarDireccionIngresada(self)

class TelefonoFormSet(BaseTelefonoFormSet):

  def clean(self):
    super(TelefonoFormSet,self).clean()
    validarTelefonoIngresado(self)

class FotoAgenciadoFormSet(BaseFotoAgenciadoFormSet):
  def clean(self):
    super(FotoAgenciadoFormSet,self).clean()
    validarFotoIngresada(self)

@login_required
def index(request):
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
