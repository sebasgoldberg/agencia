# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission, Group
from django.utils.translation import activate
from iampacks.agencia.perfil.models import Danza, Deporte, EstadoDientes, Idioma, Instrumento, Ojos, Pelo, Piel, Talle
from optparse import make_option
from django.utils.translation import ugettext as _
from django.conf import settings

class Command(BaseCommand):

  help=u'Carga datos de perfiles'

  option_list = BaseCommand.option_list + (
    make_option('--idioma'),
    )

  def load_perfil_for_language(self,language):

    activate(language)

    Pelo(descripcion=_(u'Castanho')).save()
    Pelo(descripcion=_(u'Castanho Claro')).save()
    Pelo(descripcion=_(u'Grisalho')).save()
    Pelo(descripcion=_(u'Loiro')).save()
    Pelo(descripcion=_(u'Preto')).save()
    Pelo(descripcion=_(u'Preto Claro')).save()
    Pelo(descripcion=_(u'Ruiva')).save()

    Danza(descripcion=_(u'Ballet')).save()
    Danza(descripcion=_(u'Dança')).save()
    Danza(descripcion=_(u'Dança de Rua')).save()
    Danza(descripcion=_(u'Hip Hop')).save()
    Danza(descripcion=_(u'Jazz')).save()
    Danza(descripcion=_(u'Sapateado')).save()
    Danza(descripcion=_(u'Street Dance')).save()
    Danza(descripcion=_(u'Ventre')).save()
    Danza(descripcion=_(u'Gafieira')).save()
    
    Deporte(descripcion=_(u'Aeróbica')).save()
    Deporte(descripcion=_(u'Anda a Cavalo')).save()
    Deporte(descripcion=_(u'Atletismo')).save()
    Deporte(descripcion=_(u'Ator')).save()
    Deporte(descripcion=_(u'Basquete')).save()
    Deporte(descripcion=_(u'Bicicleta')).save()
    Deporte(descripcion=_(u'Boliche')).save()
    Deporte(descripcion=_(u'Capoeira')).save()
    Deporte(descripcion=_(u'Cavalgar')).save()
    Deporte(descripcion=_(u'Ciclismo')).save()
    Deporte(descripcion=_(u'Corrida c/ obstáculo')).save()
    Deporte(descripcion=_(u'Dança')).save()
    Deporte(descripcion=_(u'Futebol')).save()
    Deporte(descripcion=_(u'Futsal')).save()
    Deporte(descripcion=_(u'Ginastica Artistica')).save()
    Deporte(descripcion=_(u'Ginastica Acrobática')).save()
    Deporte(descripcion=_(u'Ginastica Olimpica')).save()
    Deporte(descripcion=_(u'Ginastica Ritmica')).save()
    Deporte(descripcion=_(u'Handeboll')).save()
    Deporte(descripcion=_(u'Judo')).save()
    Deporte(descripcion=_(u'Karate')).save()
    Deporte(descripcion=_(u'Kung-fu')).save()
    Deporte(descripcion=_(u'Locução')).save()
    Deporte(descripcion=_(u'Maaythay')).save()
    Deporte(descripcion=_(u'Natação')).save()
    Deporte(descripcion=_(u'Patinação Artística')).save()
    Deporte(descripcion=_(u'Patins')).save()
    Deporte(descripcion=_(u'Power Jump')).save()
    Deporte(descripcion=_(u'Rooler')).save()
    Deporte(descripcion=_(u'samba')).save()
    Deporte(descripcion=_(u'Skate')).save()
    Deporte(descripcion=_(u'streetdance')).save()
    Deporte(descripcion=_(u'Surf')).save()
    Deporte(descripcion=_(u'Taekondo')).save()
    Deporte(descripcion=_(u'Teatro')).save()
    Deporte(descripcion=_(u'Tenis')).save()
    Deporte(descripcion=_(u'Vôlei')).save()

    EstadoDientes(descripcion=_(u'Bom')).save()
    EstadoDientes(descripcion=_(u'Sem informação')).save()
    
    Idioma(descripcion=_(u'Alemao')).save()
    Idioma(descripcion=_(u'Chino')).save()
    Idioma(descripcion=_(u'Espanhol')).save()
    Idioma(descripcion=_(u'Francês')).save()
    Idioma(descripcion=_(u'Inglês')).save()
    Idioma(descripcion=_(u'Inglês intermediario')).save()
    Idioma(descripcion=_(u'Italiano')).save()
    Idioma(descripcion=_(u'Japones')).save()
    
    Instrumento(descripcion=_(u'Acordeon')).save()
    Instrumento(descripcion=_(u'Agogo')).save()
    Instrumento(descripcion=_(u'Birimbal')).save()
    Instrumento(descripcion=_(u'Canto')).save()
    Instrumento(descripcion=_(u'Chocalho')).save()
    Instrumento(descripcion=_(u'Escaleta')).save()
    Instrumento(descripcion=_(u'Flauta')).save()
    Instrumento(descripcion=_(u'Guitara')).save()
    Instrumento(descripcion=_(u'Lira')).save()
    Instrumento(descripcion=_(u'Orgão')).save()
    Instrumento(descripcion=_(u'Pandeiro')).save()
    Instrumento(descripcion=_(u'Percussão')).save()
    Instrumento(descripcion=_(u'Piano')).save()
    Instrumento(descripcion=_(u'Sino')).save()
    Instrumento(descripcion=_(u'Tambor')).save()
    Instrumento(descripcion=_(u'Teclado')).save()
    Instrumento(descripcion=_(u'Timba')).save()
    Instrumento(descripcion=_(u'Triângulo')).save()
    Instrumento(descripcion=_(u'Trompete')).save()
    Instrumento(descripcion=_(u'Violão')).save()
    Instrumento(descripcion=_(u'Violino')).save()
    
    Talle(descripcion=_(u'Robusta')).save()
    Talle(descripcion=_(u'Gordo')).save()
    Talle(descripcion=_(u'Flaco')).save()
    Talle(descripcion=_(u'Atletica')).save()
    Talle(descripcion=_(u'Musculosa')).save()
    Talle(descripcion=_(u'Normal')).save()
    
    Ojos(descripcion=_(u'Azul')).save()
    Ojos(descripcion=_(u'Bermelhos')).save()
    Ojos(descripcion=_(u'Castanho')).save()
    Ojos(descripcion=_(u'Castanho Claro')).save()
    Ojos(descripcion=_(u'Preto')).save()
    Ojos(descripcion=_(u'Verdes')).save()
    
    Piel(descripcion=_(u'Branca')).save()
    Piel(descripcion=_(u'Morena')).save()
    Piel(descripcion=_(u'Negra')).save()
    Piel(descripcion=_(u'Oriental')).save()
    Piel(descripcion=_(u'Parda')).save()


  def handle(self,*args,**options):

    for (lang_code,_) in settings.LANGUAGES:
      self.load_perfil_for_language(lang_code)

    self.stdout.write('Datos de perfiles cargados con exito.\n')


