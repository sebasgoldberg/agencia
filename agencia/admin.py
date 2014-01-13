# coding=utf-8
from iampacks.agencia.agencia.models import Agenciado, FotoAgenciado, VideoAgenciado, Telefono, validarTelefonoIngresado, validarFotoIngresada, DireccionAgenciado, Agencia, TelefonoAgencia, DireccionAgencia
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from iampacks.cross.direccion.admin import PaisDireccionModelListFilter, EstadoDireccionModelListFilter, CiudadDireccionModelListFilter, BaseDireccionInline
from iampacks.agencia.agencia.forms import DireccionAgenciaForm, DireccionAgenciadoForm
from django.contrib.sites.models import Site
from cities_light.models import Country, Region, City

class DireccionAgenciaInline(BaseDireccionInline):
  form = DireccionAgenciaForm
  model=DireccionAgencia
  extra = 1
  max_num = 1

class TelefonoAgenciaInline(admin.TabularInline):
  model=TelefonoAgencia
  extra=1

class AgenciaAdmin(admin.ModelAdmin):
  inlines=[DireccionAgenciaInline, TelefonoAgenciaInline]
  list_display=['id','nombre','email','activa']
  list_display_links = ('id', 'nombre')
  list_filter=['activa']
  search_fields=['nombre']
  list_per_page = 40
  exclude=['logo']

class TelefonoFormSet(BaseInlineFormSet):
  def clean(self):
    super(TelefonoFormSet,self).clean()
    validarTelefonoIngresado(self)

class FotoAgenciadoFormSet(BaseInlineFormSet):
  def clean(self):
    super(FotoAgenciadoFormSet,self).clean()

class DireccionAgenciadoInline(BaseDireccionInline):
  form = DireccionAgenciadoForm
  model=DireccionAgenciado
  extra = 1
  max_num = 1
  can_delete=False

class TelefonoInline(admin.TabularInline):
  model=Telefono
  extra=1
  max_num=6
  formset=TelefonoFormSet

class FotoAgenciadoInline(admin.TabularInline):
  model=FotoAgenciado
  extra=1
  max_num=6
  formset=FotoAgenciadoFormSet

class VideoAgenciadoInline(admin.TabularInline):
  model=VideoAgenciado
  exclude = ['codigo_video']
  extra=1
  max_num=6


class PaisDireccionAgenciadoListFilter(PaisDireccionModelListFilter):
  direccion_model = DireccionAgenciado
  fk_field_model = 'agenciado'

class EstadoDireccionAgenciadoListFilter(EstadoDireccionModelListFilter):
  direccion_model = DireccionAgenciado
  fk_field_model = 'agenciado'

class CiudadDireccionAgenciadoListFilter(CiudadDireccionModelListFilter):
  direccion_model = DireccionAgenciado
  fk_field_model = 'agenciado'

class AgenciadoAdmin(admin.ModelAdmin):
  readonly_fields=['id','thumbnails']
  fieldsets=[
    (None, {'fields':['thumbnails','id','mail']}),
    (_(u'Dados Pessoales'), {'fields':[('nombre', 'apellido', 'fecha_nacimiento')]}),
    (_(u'Dados Administrativos'), { 'fields':[ ('documento_rg', 'documento_cpf'), 'responsable', 'cuenta_bancaria']}),
    (None, {"classes": ("placeholder telefono_set-group",), "fields" : ()}),
    (None, {"classes": ("placeholder direccionagenciado_set-group",), "fields" : ()}),
    (None, {"classes": ("placeholder fotoagenciado_set-group",), "fields" : ()}),
    (None, {"classes": ("placeholder videoagenciado_set-group",), "fields" : ()}),
    # @todo comentar
    #(_(u'Dados de endereço'), { 'fields':[ ('estado', 'ciudad', 'barrio'), ('direccion', 'codigo_postal')]}),
    (_(u'Carateristicas fisicas'), { 'fields':[ 
      'sexo', 
      ('ojos', 'pelo', 'piel', ), 
      ('altura', 'peso', 'talle',), 
      ( 'talle_camisa', 'talle_pantalon', 'calzado'),
      'estado_dientes',]}),
    (_(u'Habilidades'),{
      'classes': ('grp-collapse grp-closed',),
      'fields':[ 'deportes', 'danzas', 'instrumentos', 'idiomas', ('indicador_maneja', 'indicador_tiene_registro')]
      }),
    (_(u'Otros dados'), { 
      'classes': ('grp-collapse grp-closed',),
      'fields':[ 'trabaja_como_extra', 'como_nos_conocio', 'observaciones', 'activo', 'fecha_ingreso']
      }),
  ]
  # @todo Descomentar
  inlines=[DireccionAgenciadoInline, TelefonoInline, FotoAgenciadoInline, VideoAgenciadoInline]
  list_display=['thumbnail','id','apellido','nombre','fecha_nacimiento','descripcion','telefonos','mail', 'responsable']
  list_display_links = ('thumbnail', 'id')
  list_filter=['activo','sexo','ojos','pelo','piel','deportes','danzas','instrumentos','idiomas','fecha_ingreso',PaisDireccionAgenciadoListFilter, EstadoDireccionAgenciadoListFilter, CiudadDireccionAgenciadoListFilter]
  search_fields=['nombre','apellido','responsable','mail','id']
  date_hierarchy='fecha_nacimiento'
  filter_horizontal=['deportes','danzas','instrumentos','idiomas']
  list_per_page = 40
  actions_on_bottom = True

from django.contrib.admin.sites import AlreadyRegistered, NotRegistered

def register_even_registered(model,model_admin):
  try:
    admin.site.register(model,model_admin)
  except AlreadyRegistered:
    pass

def unregister_even_not_registered(model):
  try:
    admin.site.unregister(model)
  except NotRegistered:
    pass
  

register_even_registered(Agenciado,AgenciadoAdmin)
register_even_registered(Agencia,AgenciaAdmin)
unregister_even_not_registered(Site)
unregister_even_not_registered(Country)
unregister_even_not_registered(Region)
unregister_even_not_registered(City)
