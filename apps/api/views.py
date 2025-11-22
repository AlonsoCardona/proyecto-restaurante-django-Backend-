from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.ordenes.models import DetalleOrden
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import OrdenDetalleSerializer

class OrdenDetalleListAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        orden_detalles = DetalleOrden.objects.filter(orden__estado='pendiente')
        serializer = OrdenDetalleSerializer(orden_detalles, many=True)
        return Response(serializer.data)

