from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('ordenes-pendientes/', views.OrdenDetalleListAPIView.as_view(), name='orden_detalle_list'),
]

