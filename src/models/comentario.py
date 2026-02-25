from django.db import models
from django.utils.translation import gettext_lazy as _
from .usuario import Usuario
from .publicacion import Publicacion

class Comentario(models.Model):
    """
    Modelo de Comentario con soporte para hilos (threading)
    """
    
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name=_("Publicación")
    )
    
    creador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name=_("Autor")
    )
    
    contenido = models.TextField(
        verbose_name=_("Contenido del comentario")
    )
    
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha")
    )
    
    # Para hilos de comentarios (comentario padre)
    referencia_comentario_raiz = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='respuestas',
        verbose_name=_("Comentario raíz")
    )
    
    class Meta:
        verbose_name = _("Comentario")
        verbose_name_plural = _("Comentarios")
        ordering = ['fecha']
    
    def __str__(self):
        return f"{self.creador.username} - {self.contenido[:50]}"
    
    def is_respuesta(self):
        """Verifica si es una respuesta a otro comentario"""
        return self.referencia_comentario_raiz is not None