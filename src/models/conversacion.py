from django.db import models
from django.utils.translation import gettext_lazy as _
from .usuario import Usuario

class Conversacion(models.Model):
    """
    Modelo de Conversación entre dos usuarios
    """
    participante_1 = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='conversaciones_iniciadas',
        verbose_name=_("Participante 1")
    )
    
    participante_2 = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='conversaciones_recibidas',
        verbose_name=_("Participante 2")
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación")
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Última actualización")
    )
    
    class Meta:
        verbose_name = _("Conversación")
        verbose_name_plural = _("Conversaciones")
        ordering = ['-fecha_actualizacion']
        unique_together = ['participante_1', 'participante_2']
    
    def __str__(self):
        return f"{self.participante_1.get_full_name()} - {self.participante_2.get_full_name()}"
    
    def get_otro_participante(self, usuario):
        """Retorna el otro participante de la conversación"""
        return self.participante_2 if self.participante_1 == usuario else self.participante_1
    
    def get_ultimo_mensaje(self):
        """Retorna el último mensaje de la conversación"""
        return self.mensajes.order_by('-fecha_envio').first()
    
    def mensajes_no_leidos(self, usuario):
        """Cuenta mensajes no leídos para un usuario"""
        return self.mensajes.filter(
            receptor=usuario,
            leido=False
        ).count()