import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear superusuario si no existe
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@izakayasakura.com',
        password='admin123',
        first_name='Administrador',
        last_name='Sistema'
    )
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print('✅ Superusuario creado: admin / admin123')
else:
    print('ℹ️ El superusuario ya existe')
