from rest_framework import serializers
from apps.ordenes.models import DetalleOrden
from apps.platillos.models import Platillo

class PlatilloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platillo
        fields = ['nombre']

class OrdenDetalleSerializer(serializers.ModelSerializer):
    platillo = PlatilloSerializer(read_only=True)
    class Meta:
        model = DetalleOrden
        fields = ['platillo','cantidad','notas']

