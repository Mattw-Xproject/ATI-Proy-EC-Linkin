from django.db import models
from django.utils.translation import gettext_lazy as _
from .profesional import Profesional

class Habilidad(models.Model):
    """
    Habilidades/Skills de un profesional
    """
    profesional = models.ForeignKey(
        Profesional,
        on_delete=models.CASCADE,
        related_name='habilidades',
        verbose_name=_("Profesional")
    )
    
    nombre = models.CharField(
        max_length=100,
        verbose_name=_("Nombre de la habilidad")
    )
    
    nivel = models.CharField(
        max_length=20,
        choices=[
            ('basico', _('Básico')),
            ('intermedio', _('Intermedio')),
            ('avanzado', _('Avanzado')),
            ('experto', _('Experto')),
        ],
        default='intermedio',
        verbose_name=_("Nivel")
    )
    
    fecha_agregada = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha agregada")
    )
    
    class Meta:
        verbose_name = _("Habilidad")
        verbose_name_plural = _("Habilidades")
        ordering = ['-fecha_agregada']
        unique_together = ['profesional', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.nivel})"