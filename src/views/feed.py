from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Exists, OuterRef
from django.utils.translation import gettext as _
from src.models import Publicacion, Comentario, Like, Seguidor, Usuario

@login_required
def feed_home(request):
    """
    Vista principal del feed
    """
    # Obtener todas las publicaciones con contadores
    publicaciones = Publicacion.objects.select_related(
        'autor'
    ).annotate(
        total_likes=Count('likes', distinct=True),
        total_comentarios=Count('comentarios', distinct=True),
        usuario_dio_like=Exists(
            Like.objects.filter(
                publicacion=OuterRef('pk'),
                usuario=request.user
            )
        )
    ).order_by('-fecha_creacion')[:50]
    
    # Agregar información de seguimiento para cada publicación
    for pub in publicaciones:
        pub.usuario_sigue_autor = Seguidor.objects.filter(
            seguidor=request.user,
            seguido=pub.autor
        ).exists()
    
    context = {
        'publicaciones': publicaciones,
    }
    
    return render(request, 'feed/feed_home.html', context)


@login_required
def crear_publicacion(request):
    """
    Vista para crear una nueva publicación
    """
    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        imagen = request.FILES.get('imagen')
        video = request.FILES.get('video')
        
        if contenido or imagen or video:
            publicacion = Publicacion.objects.create(
                autor=request.user,
                contenido=contenido,
                imagen=imagen,
                video=video
            )
            return redirect('feed_home')
    
    return redirect('feed_home')


@login_required
def toggle_like(request, publicacion_id):
    """
    Vista para dar/quitar like a una publicación
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    
    like, created = Like.objects.get_or_create(
        usuario=request.user,
        publicacion=publicacion
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    # Obtener nuevo total de likes
    total_likes = publicacion.likes.count()
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'total_likes': total_likes
    })


@login_required
def crear_comentario(request, publicacion_id):
    """
    Vista para crear un comentario
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    contenido = request.POST.get('contenido', '').strip()
    comentario_padre_id = request.POST.get('comentario_padre_id')
    
    if not contenido:
        return JsonResponse({'error': 'Contenido vacío'}, status=400)
    
    comentario_padre = None
    if comentario_padre_id:
        comentario_padre = get_object_or_404(Comentario, id=comentario_padre_id)
    
    comentario = Comentario.objects.create(
        publicacion=publicacion,
        autor=request.user,
        contenido=contenido,
        comentario_padre=comentario_padre
    )
    
    return JsonResponse({
        'success': True,
        'comentario': {
            'id': comentario.id,
            'autor': comentario.autor.get_full_name(),
            'autor_avatar': comentario.autor.get_avatar_url(),
            'contenido': comentario.contenido,
            'nivel': comentario.get_nivel_visual(),
            'fecha': comentario.fecha_creacion.strftime('%d %b %Y'),
        },
        'total_comentarios': publicacion.comentarios.count()
    })


@login_required
def toggle_seguir(request, usuario_id):
    """
    Vista para seguir/dejar de seguir a un usuario
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    usuario_a_seguir = get_object_or_404(Usuario, id=usuario_id)
    
    if usuario_a_seguir == request.user:
        return JsonResponse({'error': 'No puedes seguirte a ti mismo'}, status=400)
    
    seguidor, created = Seguidor.objects.get_or_create(
        seguidor=request.user,
        seguido=usuario_a_seguir
    )
    
    if not created:
        seguidor.delete()
        siguiendo = False
    else:
        siguiendo = True
    
    return JsonResponse({
        'success': True,
        'siguiendo': siguiendo
    })


@login_required
def cargar_comentarios(request, publicacion_id):
    """
    Vista para cargar comentarios de una publicación
    """
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    
    # Obtener comentarios de nivel 0 (raíz)
    comentarios_raiz = publicacion.comentarios.filter(
        comentario_padre__isnull=True
    ).select_related('autor').order_by('fecha_creacion')
    
    def serializar_comentario(comentario):
        return {
            'id': comentario.id,
            'autor': comentario.autor.get_full_name(),
            'autor_avatar': comentario.autor.get_avatar_url(),
            'contenido': comentario.contenido,
            'fecha': comentario.fecha_creacion.strftime('%d %b %Y'),
            'nivel': comentario.get_nivel_visual(),
            'respuestas': [serializar_comentario(resp) for resp in comentario.get_respuestas()]
        }
    
    comentarios_data = [serializar_comentario(c) for c in comentarios_raiz]
    
    return JsonResponse({
        'success': True,
        'comentarios': comentarios_data,
        'total': publicacion.comentarios.count()
    })