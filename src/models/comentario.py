from django.db import models
from django.utils.translation import gettext_lazy as _
from .usuario import Usuario
from .publicacion import Publicacion

class Comentario(models.Model):
    """
    Modelo de Comentario con soporte para anidación
    """
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name=_("Publicación")
    )
    
    autor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='comentarios',
        verbose_name=_("Autor")
    )
    
    contenido = models.TextField(
        verbose_name=_("Contenido")
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de creación")
    )
    
    # Para comentarios anidados
    comentario_padre = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name=_("Comentario padre")
    )
    
    nivel = models.IntegerField(
        default=0,
        verbose_name=_("Nivel de anidación")
    )
    
    class Meta:
        verbose_name = _("Comentario")
        verbose_name_plural = _("Comentarios")
        ordering = ['fecha_creacion']
    
    def __str__(self):
        return f"Comentario de {self.autor.get_full_name()} en {self.publicacion}"
    
    def save(self, *args, **kwargs):
        """Calcular el nivel de anidación automáticamente"""
        if self.comentario_padre:
            self.nivel = self.comentario_padre.nivel + 1
        else:
            self.nivel = 0
        super().save(*args, **kwargs)
    
    def get_nivel_visual(self):
        """Retorna el nivel visual (máximo 3 para UI)"""
        return min(self.nivel, 3)
    
    def get_respuestas(self):
        """Retorna las respuestas directas a este comentario"""
        return self.respuestas.all()