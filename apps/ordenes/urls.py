from django.urls import path
from . import views

app_name = 'ordenes'

urlpatterns = [
    path('mesas_estado/', views.MesaEstadoListView.as_view(), name='mesas_estado_list'),
    path('mesas_estado/nuevo/', views.MesaEstadoCreateView.as_view(), name='mesas_estado_create'),
    path('mesas_estado/editar/<int:pk>/', views.MesaEstadoUpdateView.as_view(), name='mesas_estado_update'),
    path('mesas_estado/eliminar/<int:pk>/', views.MesaEstadoDeleteView.as_view(), name='mesas_estado_delete'),
    path('mesas/', views.MesaListView.as_view(), name='mesas_list'),
    path('mesas/nuevo/', views.MesaCreateView.as_view(), name='mesas_create'),
    path('mesas/editar/<int:pk>/', views.MesaUpdateView.as_view(), name='mesas_update'),
    path('mesas/eliminar/<int:pk>/', views.MesaDeleteView.as_view(), name='mesas_delete'),
    path('ordenes/', views.OrdenListView.as_view(), name='orden_list'),
    path('ordenes/nuevo/', views.OrdenCreateView.as_view(), name='orden_create'),
    path('ordenes/editar/<int:pk>/', views.OrdenUpdateView.as_view(), name='orden_update'),
    path('ordenes/eliminar/<int:pk>/', views.OrdenDeleteView.as_view(), name='orden_delete'),
    path('ordenes/<int:orden_id>/detalles/', views.OrdenDetalleView.as_view(), name='orden_detalle_list'),
    path('ordenes/<int:pk>/detalles/edit/', views.OrdenDetalleUpdateView.as_view(), name='orden_detalle_update'),
    path('ordenes/detalles/eliminar/<int:pk>/', views.OrdenDetalleDeleteView.as_view(), name='orden_detalle_delete'),
    path('ordenes/<int:orden_id>/pagar/', views.OrdenPagarView.as_view(), name='orden_pagar'),
    path('metodos_pago/', views.MetodoPagoListView.as_view(), name='metodos_pago_list'),
    path('metodos_pago/nuevo/', views.MetodoPagoCreateView.as_view(), name='metodos_pago_create'),
    path('metodos_pago/editar/<int:pk>/', views.MetodoPagoUpdateView.as_view(), name='metodos_pago_edit'),
    path('metodos_pago/eliminar/<int:pk>/', views.MetodoPagoDeleteView.as_view(), name='metodos_pago_delete'),
    path('pagos/', views.PagoListView.as_view(), name='pagos_list'),
]