from django.db import models
from apps.platillos.models import Platillo
from apps.accounts.models import AppUser

class MesaEstado(models.Model):
    COLOR_CHOICES = [
        ('rojo', 'Rojo'),
        ('verde', 'Verde'),
        ('amarillo', 'Amarillo'),
    ]
    
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='verde')

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    capacidad = models.IntegerField(null=False)
    estado = models.ForeignKey(MesaEstado, on_delete=models.CASCADE, related_name='mesas_estado')

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_preparacion', 'En Preparación'),
        ('servida', 'Servida'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada'),
    ]
    
    empleado = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='ordenes')
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='ordenes')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Orden #{self.id} - Mesa {self.mesa.nombre}"
    
    def calcular_total(self):
        total = sum(detalle.subtotal for detalle in self.detalles.all())
        self.total = total
        self.save()
        return total

class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    notas = models.TextField(blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad}x {self.platillo.nombre}"
    
    def save(self, *args, **kwargs):
        self.precio_unitario = self.platillo.precio
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.orden.calcular_total()

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Pago(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, related_name='pagos')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pago de ${self.cantidad} - Orden #{self.orden.id}"

