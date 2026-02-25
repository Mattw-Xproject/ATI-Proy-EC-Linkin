from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    """
    Modelo extendido de Usuario basado en el diagrama de dominio.
    Campos heredados: username, password, email, first_name, last_name
    """
    
    # Campos adicionales del modelo de dominio
    foto = models.ImageField(
        upload_to='usuarios/avatars/',
        null=True,
        blank=True,
        verbose_name=_("Foto de perfil")
    )
    
    ubicacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Ubicación")
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de registro")
    )
    
    # Tipo de usuario (para diferenciar Profesional vs Empresa)
    TIPO_CHOICES = [
        ('profesional', _('Profesional')),
        ('empresa', _('Empresa')),
    ]
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Tipo de usuario")
    )
    
    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    def get_avatar_url(self):
        """Retorna URL del avatar o placeholder"""
        if self.foto:
            return self.foto.url
        return '/static/img/placeholder-avatar.png'