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

def index(request): 
  return render(request,'reliquia/index.html')
