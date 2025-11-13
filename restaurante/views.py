from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, Max, Min
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict
from apps.ordenes.models import Orden, DetalleOrden
from apps.platillos.models import Platillo


def main_index(request):
    return render(request, 'main/index.html')

def menu_view(request):
    return render(request, 'main/menu.html')

def contacto_view(request):
    return render(request, 'main/contacto.html')

@login_required
def perfil_view(request):
    return render(request, 'main/perfil.html')

@login_required
def dashboard_view(request):
    ahora = timezone.now()
    hoy_inicio = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    hoy_fin = ahora.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    # === MÉTRICAS DEL DÍA ACTUAL ===
    ventas_hoy = Orden.objects.filter(
        fecha__range=(hoy_inicio, hoy_fin)
    ).aggregate(
        total_vendido=Sum('total'),
        total_ordenes=Count('id')
    )
    
    efectivo_hoy = ventas_hoy['total_vendido'] if ventas_hoy['total_vendido'] else 0
    pedidos_hoy = ventas_hoy['total_ordenes']
    
    # === ANÁLISIS SEMANAL (7 días atrás desde hoy) ===
    hace_semana = hoy_inicio - timedelta(days=7)
    resumen_semanal = Orden.objects.filter(
        fecha__gte=hace_semana
    ).aggregate(total_semanal=Sum('total'))
    
    dinero_semana = resumen_semanal['total_semanal'] if resumen_semanal['total_semanal'] else 0
    
    # === HISTORIAL RECIENTE (5 transacciones más nuevas) ===
    historial_reciente = list(
        Orden.objects
        .select_related('mesa')
        .prefetch_related('detalles')
        .order_by('-id')[:5]
        .values('id', 'mesa__nombre', 'fecha', 'total')
    )
    
    # === RANKING DE PRODUCTOS (5 favoritos) ===
    ranking_productos = list(
        DetalleOrden.objects
        .values('platillo__nombre')
        .annotate(cantidad_total=Sum('cantidad'))
        .order_by('-cantidad_total')[:5]
    )
    
    datos_dashboard = {
        'efectivo_hoy': efectivo_hoy,
        'pedidos_hoy': pedidos_hoy,
        'dinero_semana': dinero_semana,
        'historial_reciente': historial_reciente,
        'ranking_productos': ranking_productos,
    }
    
    return render(request, 'main/dashboard.html', datos_dashboard)