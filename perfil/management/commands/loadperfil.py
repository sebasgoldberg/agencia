# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission, Group
from django.utils.translation import activate, get_language
from iampacks.agencia.perfil.models import Danza, Deporte, EstadoDientes, Idioma, Instrumento, Ojos, Pelo, Piel, Talle
from optparse import make_option
from django.utils.translation import ugettext
from django.conf import settings

class Command(BaseCommand):

  help=u'Carga datos de perfiles'

  option_list = BaseCommand.option_list + (
    make_option('--idioma'),
    )

  def load_entity(self,Class,descripcion):
    
    instance,created=Class.objects.get_or_create(descripcion=descripcion)
    current_language=get_language()
    for (lang_code,_) in settings.LANGUAGES:
      activate(lang_code)
      instance.descripcion = ugettext(descripcion)
    activate(current_language)
    instance.save()

  def load_perfil_for_language(self):

    self.load_entity(Pelo,u'Castanho')
    self.load_entity(Pelo,u'Castanho Claro')
    self.load_entity(Pelo,u'Grisalho')
    self.load_entity(Pelo,u'Loiro')
    self.load_entity(Pelo,u'Preto')
    self.load_entity(Pelo,u'Preto Claro')
    self.load_entity(Pelo,u'Ruiva')

    self.load_entity(Danza,u'Ballet')
    self.load_entity(Danza,u'Dança')
    self.load_entity(Danza,u'Dança de Rua')
    self.load_entity(Danza,u'Hip Hop')
    self.load_entity(Danza,u'Jazz')
    self.load_entity(Danza,u'Sapateado')
    self.load_entity(Danza,u'Street Dance')
    self.load_entity(Danza,u'Ventre')
    self.load_entity(Danza,u'Gafieira')
    
    self.load_entity(Deporte,u'Aeróbica')
    self.load_entity(Deporte,u'Anda a Cavalo')
    self.load_entity(Deporte,u'Atletismo')
    self.load_entity(Deporte,u'Ator')
    self.load_entity(Deporte,u'Basquete')
    self.load_entity(Deporte,u'Bicicleta')
    self.load_entity(Deporte,u'Boliche')
    self.load_entity(Deporte,u'Capoeira')
    self.load_entity(Deporte,u'Cavalgar')
    self.load_entity(Deporte,u'Ciclismo')
    self.load_entity(Deporte,u'Corrida c/ obstáculo')
    self.load_entity(Deporte,u'Dança')
    self.load_entity(Deporte,u'Futebol')
    self.load_entity(Deporte,u'Futsal')
    self.load_entity(Deporte,u'Ginastica Artistica')
    self.load_entity(Deporte,u'Ginastica Acrobática')
    self.load_entity(Deporte,u'Ginastica Olimpica')
    self.load_entity(Deporte,u'Ginastica Ritmica')
    self.load_entity(Deporte,u'Handeboll')
    self.load_entity(Deporte,u'Judo')
    self.load_entity(Deporte,u'Karate')
    self.load_entity(Deporte,u'Kung-fu')
    self.load_entity(Deporte,u'Locução')
    self.load_entity(Deporte,u'Maaythay')
    self.load_entity(Deporte,u'Natação')
    self.load_entity(Deporte,u'Patinação Artística')
    self.load_entity(Deporte,u'Patins')
    self.load_entity(Deporte,u'Power Jump')
    self.load_entity(Deporte,u'Rooler')
    self.load_entity(Deporte,u'samba')
    self.load_entity(Deporte,u'Skate')
    self.load_entity(Deporte,u'streetdance')
    self.load_entity(Deporte,u'Surf')
    self.load_entity(Deporte,u'Taekondo')
    self.load_entity(Deporte,u'Teatro')
    self.load_entity(Deporte,u'Tenis')
    self.load_entity(Deporte,u'Vôlei')

    self.load_entity(EstadoDientes,u'Bom')
    self.load_entity(EstadoDientes,u'Sem informação')
    
    self.load_entity(Idioma,u'Alemao')
    self.load_entity(Idioma,u'Chino')
    self.load_entity(Idioma,u'Espanhol')
    self.load_entity(Idioma,u'Francês')
    self.load_entity(Idioma,u'Inglês')
    self.load_entity(Idioma,u'Inglês intermediario')
    self.load_entity(Idioma,u'Italiano')
    self.load_entity(Idioma,u'Japones')
    
    self.load_entity(Instrumento,u'Acordeon')
    self.load_entity(Instrumento,u'Agogo')
    self.load_entity(Instrumento,u'Birimbal')
    self.load_entity(Instrumento,u'Canto')
    self.load_entity(Instrumento,u'Chocalho')
    self.load_entity(Instrumento,u'Escaleta')
    self.load_entity(Instrumento,u'Flauta')
    self.load_entity(Instrumento,u'Lira')
    self.load_entity(Instrumento,u'Orgão')
    self.load_entity(Instrumento,u'Pandeiro')
    self.load_entity(Instrumento,u'Percussão')
    self.load_entity(Instrumento,u'Piano')
    self.load_entity(Instrumento,u'Sino')
    self.load_entity(Instrumento,u'Tambor')
    self.load_entity(Instrumento,u'Teclado')
    self.load_entity(Instrumento,u'Timba')
    self.load_entity(Instrumento,u'Triângulo')
    self.load_entity(Instrumento,u'Trompete')
    self.load_entity(Instrumento,u'Violão')
    self.load_entity(Instrumento,u'Violino')

    self.load_entity(Talle,u'Robusta')
    self.load_entity(Talle,u'Gordo')
    self.load_entity(Talle,u'Flaco')
    self.load_entity(Talle,u'Atletica')
    self.load_entity(Talle,u'Musculosa')
    self.load_entity(Talle,u'Normal')

    self.load_entity(Ojos,u'Azul')
    self.load_entity(Ojos,u'Bermelhos')
    self.load_entity(Ojos,u'Castanho')
    self.load_entity(Ojos,u'Castanho Claro')
    self.load_entity(Ojos,u'Preto')
    self.load_entity(Ojos,u'Verdes')

    self.load_entity(Piel,u'Branca')
    self.load_entity(Piel,u'Morena')
    self.load_entity(Piel,u'Negra')
    self.load_entity(Piel,u'Oriental')
    self.load_entity(Piel,u'Parda')

  def handle(self,*args,**options):

    self.load_perfil_for_language()

    self.stdout.write('Datos de perfiles cargados con exito.\n')


