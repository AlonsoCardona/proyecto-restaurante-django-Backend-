from django.contrib import admin
from .models import MesaEstado, Mesa, Orden, DetalleOrden, MetodoPago, Pago

admin.site.register(MesaEstado)
admin.site.register(Mesa)
admin.site.register(Orden)
admin.site.register(DetalleOrden)
admin.site.register(MetodoPago)
admin.site.register(Pago)
