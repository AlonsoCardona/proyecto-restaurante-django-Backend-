from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    # AbstractUser ya incluye: username, email, password, first_name, last_name
    # No necesitamos agregar campos adicionales por ahora
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
