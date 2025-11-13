from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .models import Mesa, MesaEstado, Orden, DetalleOrden, MetodoPago, Pago
from .forms import MesaEstadoForm, MesaForm, OrdenForm, OrdenDetalleForm, MetodoPagoForm, PagoForm

class MesaEstadoListView(LoginRequiredMixin, ListView):
    model = MesaEstado
    template_name = 'mesas/mesas_estado_list.html'
    context_object_name = 'mesas_estados'

class MesaEstadoCreateView(LoginRequiredMixin, CreateView):
    model = MesaEstado
    form_class = MesaEstadoForm
    template_name = 'mesas/mesas_estado_form.html'
    success_url = '/ordenes/mesas_estado/'

class MesaEstadoUpdateView(LoginRequiredMixin, UpdateView):
    model = MesaEstado
    form_class = MesaEstadoForm
    template_name = 'mesas/mesas_estado_edit_form.html'
    success_url = '/ordenes/mesas_estado/'

class MesaEstadoDeleteView(LoginRequiredMixin, DeleteView):
    model = MesaEstado
    template_name = 'mesas/mesas_estado_confirm_delete.html'
    success_url = '/ordenes/mesas_estado/'

class MesaListView(LoginRequiredMixin, ListView):
    model = Mesa
    template_name = 'mesas/mesas_list.html'
    context_object_name = 'mesas'

class MesaCreateView(LoginRequiredMixin, CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'mesas/mesas_form.html'
    success_url = '/ordenes/mesas/'

class MesaUpdateView(LoginRequiredMixin, UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'mesas/mesas_edit_form.html'
    success_url = '/ordenes/mesas/'

class MesaDeleteView(LoginRequiredMixin, DeleteView):
    model = Mesa
    template_name = 'mesas/mesas_confirm_delete.html'
    success_url = '/ordenes/mesas/'

class OrdenListView(LoginRequiredMixin, ListView):
    model = Orden
    template_name = 'ordenes/orden_list.html'
    context_object_name = 'ordenes'
    ordering = ['-fecha']

class OrdenCreateView(LoginRequiredMixin, CreateView):
    model = Orden
    form_class = OrdenForm
    template_name = 'ordenes/orden_form.html'
    success_url = '/ordenes/ordenes/'

    def get_initial(self):
        initial = super().get_initial()
        initial['empleado'] = self.request.user
        return initial

class OrdenUpdateView(LoginRequiredMixin, UpdateView):
    model = Orden
    form_class = OrdenForm
    template_name = 'ordenes/orden_edit_form.html'
    success_url = '/ordenes/ordenes/'

class OrdenDeleteView(LoginRequiredMixin, DeleteView):
    model = Orden
    template_name = 'ordenes/orden_confirm_delete.html'
    success_url = '/ordenes/ordenes/'

class OrdenDetalleView(LoginRequiredMixin, ListView):
    model = DetalleOrden
    template_name = 'ordenes/orden_detalle_list.html'
    context_object_name = 'orden_detalles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = Orden.objects.get(id=self.kwargs.get('orden_id'))
        context['form'] = OrdenDetalleForm(initial={'orden_id': self.kwargs.get('orden_id')})
        return context

    def get_queryset(self):
        orden_id = self.kwargs.get('orden_id')
        return DetalleOrden.objects.filter(orden__id=orden_id)
    
    def post(self, request, *args, **kwargs):
        form = OrdenDetalleForm(request.POST)
        if form.is_valid():
            orden_detalle = DetalleOrden(
                orden=Orden.objects.get(id=form.cleaned_data['orden_id']),
                platillo=form.cleaned_data['platillo'],
                cantidad=form.cleaned_data['cantidad'],
                notas=form.cleaned_data['notas'],
                precio_unitario=form.cleaned_data['platillo'].precio
            )
            orden_detalle.save()
            return self.get(request, *args, **kwargs)
        else:
            return render(request, self.template_name, {'form': form, 'orden_detalles': self.get_queryset(), 'orden': Orden.objects.get(id=self.kwargs.get('orden_id'))})

class OrdenDetalleUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        detalle = DetalleOrden.objects.get(id=pk)
        form = OrdenDetalleForm(initial={
            'platillo': detalle.platillo,
            'cantidad': detalle.cantidad,
            'notas': detalle.notas,
            'orden_id': detalle.orden.id
        })
        return render(request, 'ordenes/orden_detalle_edit_form.html', {'form': form, 'detalle': detalle})

    def post(self, request, pk):
        detalle = DetalleOrden.objects.get(id=pk)
        form = OrdenDetalleForm(request.POST)
        if form.is_valid():
            detalle.platillo = form.cleaned_data['platillo']
            detalle.cantidad = form.cleaned_data['cantidad']
            detalle.notas = form.cleaned_data['notas']
            detalle.precio_unitario = form.cleaned_data['platillo'].precio
            detalle.save()
            return redirect('ordenes:orden_detalle_list', orden_id=detalle.orden.id)
        else:
            return render(request, 'ordenes/orden_detalle_edit_form.html', {'form': form, 'detalle': detalle})

class OrdenDetalleDeleteView(LoginRequiredMixin, DeleteView):
    model = DetalleOrden
    template_name = 'ordenes/orden_detalle_confirm_delete.html'

    def get_success_url(self):
        return f'/ordenes/ordenes/{self.object.orden.id}/detalles/'

class OrdenPagarView(LoginRequiredMixin, View):
    def get(self, request, orden_id):
        orden = Orden.objects.get(id=orden_id)
        detalles = DetalleOrden.objects.filter(orden=orden)
        total = sum(detalle.cantidad * detalle.precio_unitario for detalle in detalles)
        
        form = PagoForm(initial={'orden': orden, 'cantidad': total})

        return render(request, 'ordenes/orden_pagar.html', {'orden': orden, 'detalles': detalles, 'total': total, 'form': form})
    
    def post(self, request, orden_id):
        form = PagoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                pago = form.save(commit=False)
                pago.orden = Orden.objects.get(id=orden_id)
                pago.save()

                orden = pago.orden
                orden.estado = 'pagada'
                orden.save()

                # Liberar la mesa
                mesa = orden.mesa
                estado_disponible = MesaEstado.objects.filter(nombre__icontains='libre').first()
                if not estado_disponible:
                    # Si no existe "Libre", buscar por color verde
                    estado_disponible = MesaEstado.objects.filter(color='verde').first()
                if estado_disponible:
                    mesa.estado = estado_disponible
                    mesa.save()

                return redirect('ordenes:orden_list')
        
        orden = Orden.objects.get(id=orden_id)
        detalles = DetalleOrden.objects.filter(orden=orden)
        total = sum(detalle.cantidad * detalle.precio_unitario for detalle in detalles)
        return render(request, 'ordenes/orden_pagar.html', {'orden': orden, 'detalles': detalles, 'total': total, 'form': form})

class MetodoPagoListView(LoginRequiredMixin, ListView):
    model = MetodoPago
    template_name = 'pagos/metodos_pago_list.html'
    context_object_name = 'metodos_pago'

class MetodoPagoCreateView(LoginRequiredMixin, CreateView):
    model = MetodoPago
    form_class = MetodoPagoForm
    template_name = 'pagos/metodos_pago_form.html'
    success_url = '/ordenes/metodos_pago/'

class MetodoPagoUpdateView(LoginRequiredMixin, UpdateView):
    model = MetodoPago
    form_class = MetodoPagoForm
    template_name = 'pagos/metodos_pago_edit_form.html'
    success_url = '/ordenes/metodos_pago/'

class MetodoPagoDeleteView(LoginRequiredMixin, DeleteView):
    model = MetodoPago
    template_name = 'pagos/metodos_pago_confirm_delete.html'
    success_url = '/ordenes/metodos_pago/'

class PagoListView(LoginRequiredMixin, ListView):
    model = Pago
    template_name = 'pagos/pagos_list.html'
    context_object_name = 'pagos'
