import django.forms as forms
from .models import Mesa, MesaEstado, Orden, DetalleOrden, MetodoPago, Pago
from apps.platillos.models import Platillo

class MesaEstadoForm(forms.ModelForm):
    class Meta:
        model = MesaEstado
        fields = ['nombre', 'color']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'})
        }

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['nombre', 'capacidad', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['mesa', 'empleado']
        widgets = {
            'mesa': forms.Select(attrs={'class': 'form-control'}),
            'empleado': forms.HiddenInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar todas las mesas por ahora para debug
        if 'mesa' in self.fields:
            self.fields['mesa'].queryset = Mesa.objects.all()

    def save(self, commit=True):
        orden = super().save(commit=False)
        if commit:
            orden.estado = 'pendiente'
            orden.empleado = self.initial.get('empleado')
            orden.save()
            
            # Intentar cambiar estado de la mesa si existe el estado "Ocupada"
            try:
                mesa = orden.mesa
                estado_ocupada = MesaEstado.objects.filter(nombre__icontains='ocupada').first()
                if estado_ocupada:
                    mesa.estado = estado_ocupada
                    mesa.save()
            except:
                pass
        return orden

class OrdenDetalleForm(forms.Form):
    platillo = forms.ModelChoiceField(queryset=Platillo.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}))
    notas = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    orden_id = forms.IntegerField(widget=forms.HiddenInput())

class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['orden', 'metodo_pago', 'cantidad']
        widgets = {
            'orden': forms.HiddenInput(),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
        }