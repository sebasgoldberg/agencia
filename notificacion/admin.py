from django.contrib import admin
from iampacks.agencia.notificacion.models import NotificacionCuentaAgenciadoExistente


class NotificacionCuentaAgenciadoExistenteAdmin(admin.ModelAdmin):
  list_display=['id', 'agenciado', 'email_destinatario', 'fecha_envio']
  list_display_links = ('id', )
  date_hierarchy='fecha_envio'
  search_fields=['email_destinatario']

admin.site.register(NotificacionCuentaAgenciadoExistente, NotificacionCuentaAgenciadoExistenteAdmin)
