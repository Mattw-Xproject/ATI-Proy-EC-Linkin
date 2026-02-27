from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.db.models import Count, Q
from src.models import Publicacion, Usuario

@login_required
def feed_home(request):
    """
    Vista principal del feed (UC#03 - Publicaciones y Comentarios)
    
    Desktop: Layout 3 columnas (Sidebar Left + Feed + Sidebar Right)
    Mobile: Solo feed con bottom navigation
    """
    
    # Obtener publicaciones ordenadas por fecha (más recientes primero)
    publicaciones = Publicacion.objects.select_related(
        'creador'
    ).prefetch_related(
        'comentarios__creador',
        'comentarios__respuestas'
    ).annotate(
        comentarios_count=Count('comentarios')
    ).order_by('-fecha')[:20]  # Últimas 20 publicaciones
    
    # Estadísticas del usuario para el mini-perfil (sidebar left)
    user_stats = {
        'followers_count': 0,  # TODO: Implementar sistema de seguidores
        'following_count': 0,
        'posts_count': request.user.publicaciones.count(),
    }
    
    # Sugerencias para sidebar derecho (opcional)
    suggested_users = Usuario.objects.exclude(
        id=request.user.id
    ).filter(
        tipo_usuario='empresa'  # Sugerir empresas
    )[:3]
    
    context = {
        'publicaciones': publicaciones,
        'user_stats': user_stats,
        'suggested_users': suggested_users,
        'page_title': _('Feed'),
    }
    
    return render(request, 'feed_home.html', context)