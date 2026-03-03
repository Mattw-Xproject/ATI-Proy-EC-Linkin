from django.db import models
from django.utils.translation import gettext_lazy as _
from .usuario import Usuario

class Publicacion(models.Model):
    """
    Modelo de Publicación (UC#03 - Publicaciones y Comentarios)
    """
    
    # Cambiar 'creador' a 'autor' para consistencia con las vistas
    autor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='publicaciones',
        verbose_name=_("Autor")
    )
    
    contenido = models.TextField(
        blank=True,
        verbose_name=_("Contenido")
    )
    
    # Separar imagen y video en campos diferentes
    imagen = models.ImageField(
        upload_to='publicaciones/imagenes/',
        null=True,
        blank=True,
        verbose_name=_("Imagen")
    )
    
    video = models.FileField(
        upload_to='publicaciones/videos/',
        null=True,
        blank=True,
        verbose_name=_("Video")
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Fecha de publicación")
    )
    
    class Meta:
        verbose_name = _("Publicación")
        verbose_name_plural = _("Publicaciones")
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.autor.get_full_name()} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M')}"
    
    def get_comentarios_raiz(self):
        """Retorna solo comentarios de primer nivel (sin padre)"""
        return self.comentarios.filter(comentario_padre__isnull=True)
    
    # === NUEVAS PROPIEDADES PARA EL TEMPLATE ===
    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_comentarios(self):
        return self.comentarios.count()