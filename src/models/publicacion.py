from django.db import models
from django.utils.translation import gettext_lazy as _
from .usuario import Usuario

class Publicacion(models.Model):
    """
    Modelo de Publicación (UC#03 - Publicaciones y Comentarios)
    """
    
    creador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='publicaciones',
        verbose_name=_("Creador")
    )
    
    contenido = models.TextField(
        verbose_name=_("Contenido")
    )
    
    contenido_multimedia = models.ImageField(
        upload_to='publicaciones/',
        null=True,
        blank=True,
        verbose_name=_("Imagen o video")
    )
    
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de publicación")
    )
    
    # Métricas
    likes_count = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Cantidad de me gusta")
    )
    
    class Meta:
        verbose_name = _("Publicación")
        verbose_name_plural = _("Publicaciones")
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.creador.username} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
    
    def get_comentarios_raiz(self):
        """Retorna solo comentarios de primer nivel (sin padre)"""
        return self.comentarios.filter(referencia_comentario_raiz__isnull=True)