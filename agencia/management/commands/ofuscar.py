# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from iampacks.agencia.agencia.models import Agenciado
from django.conf import settings

minusculas='abcdefghijklmnopqrstuvwxyz'
mayusculas='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numeros='0123456789'

posicionesmin=dict([ (x[1],x[0]) for x in enumerate(minusculas) ])
posicionesmay=dict([ (x[1],x[0]) for x in enumerate(mayusculas) ])
posicionesnum=dict([ (x[1],x[0]) for x in enumerate(numeros) ])

def ofuscar(valor):
  if not valor:
    return valor
  nuevo_valor=''
  for caracter in valor:
    posicion=None
    try:
      posicion=posicionesmin[caracter]
    except KeyError:
      pass
    if posicion:
      nueva_posicion=((posicion*3)+7)%len(minusculas)
      nuevo_valor+=minusculas[nueva_posicion]
      continue
    try:
      posicion=posicionesmay[caracter]
    except KeyError:
      pass
    if posicion:
      nueva_posicion=((posicion*3)+7)%len(mayusculas)
      nuevo_valor+=mayusculas[nueva_posicion]
      continue
    try:
      posicion=posicionesnum[caracter]
    except KeyError:
      pass
    if posicion:
      nueva_posicion=((posicion*3)+7)%len(numeros)
      nuevo_valor+=numeros[nueva_posicion]
      continue
    nuevo_valor+=caracter
  return nuevo_valor
    
  

class Command(BaseCommand):

  help=u'Toma los datos reales de agenciados y los convierte en ficticios'

  def handle(self,*args,**options):
    
    if settings.AMBIENTE.productivo:
      self.stdout.write('ERROR: No se puede ejecutar este comando en ambiente productivo.\n')
      return

    for agenciado in Agenciado.objects.all():
      agenciado_anterior = str(agenciado)
      agenciado.nombre = ofuscar(agenciado.nombre)
      agenciado.apellido = ofuscar(agenciado.apellido)
      agenciado.mail = ofuscar(agenciado.mail)
      agenciado.responsable = ofuscar(agenciado.responsable)
      agenciado.documento_rg = ofuscar(agenciado.documento_rg)
      agenciado.documento_cpf = ofuscar(agenciado.documento_cpf)
      agenciado.save()
      for telefono in agenciado.telefono_set.all():
        telefono.telefono=ofuscar(telefono.telefono)
        telefono.save()
      for direccion in agenciado.direccionagenciado_set.all():
        direccion.barrio = ofuscar(direccion.barrio)
        direccion.direccion = ofuscar(direccion.direccion)
        direccion.codigo_postal = ofuscar(direccion.codigo_postal)
        direccion.save()

      self.stdout.write('Agenciado %s ofuscado con exito como %s.\n'%(agenciado_anterior,agenciado))

