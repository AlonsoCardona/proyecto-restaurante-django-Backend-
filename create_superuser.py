import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear superusuario si no existe
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@izakayasakura.com',
        password='admin123',  # CAMBIA ESTA CONTRASEÑA DESPUÉS
        nombre='Administrador',
        apellido='Sistema'
    )
    print('✅ Superusuario creado: admin / admin123')
else:
    print('ℹ️ El superusuario ya existe')
