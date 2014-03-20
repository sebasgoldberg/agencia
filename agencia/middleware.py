from iampacks.agencia.agencia.models import Agencia
from django.shortcuts import redirect

PATH_CREACION_AGENCIA = (
  '/admin/agencia/agencia/add/',
  )

class AgenciaMiddleWare:
  
  def process_request(self, request):
    if len(Agencia.objects.all()) > 0:
      return None
    if request.path in PATH_CREACION_AGENCIA:
      return None
    return redirect('/admin/agencia/agencia/add/')
