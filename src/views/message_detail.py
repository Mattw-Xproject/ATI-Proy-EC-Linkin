from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.utils.translation import gettext as _
from src.models import Conversacion, Mensaje, Usuario

@login_required
def message_detail(request, conversation_id):
    """
    Vista de detalle de una conversación
    """
    conversacion = get_object_or_404(
        Conversacion,
        Q(participante_1=request.user) | Q(participante_2=request.user),
        id=conversation_id
    )
    
    otro_usuario = conversacion.get_otro_participante(request.user)
    
    # Obtener todos los mensajes
    mensajes = conversacion.mensajes.select_related('emisor', 'receptor').all()
    
    # Marcar mensajes como leídos
    mensajes_no_leidos = mensajes.filter(receptor=request.user, leido=False)
    for mensaje in mensajes_no_leidos:
        mensaje.marcar_como_leido()
    
    # Obtener media compartida (archivos)
    media_compartida = conversacion.mensajes.exclude(archivo='').order_by('-fecha_envio')[:6]
    
    context = {
        'conversacion': conversacion,
        'otro_usuario': otro_usuario,
        'mensajes': mensajes,
        'media_compartida': media_compartida,
    }
    
    return render(request, 'messages/message_detail.html', context)

@login_required
def send_message(request, conversation_id):
    """
    Enviar un mensaje
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    conversacion = get_object_or_404(
        Conversacion,
        Q(participante_1=request.user) | Q(participante_2=request.user),
        id=conversation_id
    )
    
    contenido = request.POST.get('contenido', '').strip()
    
    if not contenido:
        return JsonResponse({'error': 'Empty message'}, status=400)
    
    otro_usuario = conversacion.get_otro_participante(request.user)
    
    mensaje = Mensaje.objects.create(
        conversacion=conversacion,
        emisor=request.user,
        receptor=otro_usuario,
        contenido=contenido,
        archivo=request.FILES.get('archivo')
    )
    
    # Actualizar fecha de conversación
    conversacion.save()
    
    return JsonResponse({
        'success': True,
        'mensaje': {
            'id': mensaje.id,
            'contenido': mensaje.contenido,
            'emisor': mensaje.emisor.get_full_name(),
            'fecha': mensaje.fecha_envio.isoformat(),
        }
    })

@login_required
def create_conversation(request, user_id):
    """
    Crear una nueva conversación o redirigir a existente
    """
    otro_usuario = get_object_or_404(Usuario, id=user_id)
    
    if otro_usuario == request.user:
        return redirect('message_list')
    
    # Buscar conversación existente (en cualquier dirección)
    conversacion = Conversacion.objects.filter(
        Q(participante_1=request.user, participante_2=otro_usuario) |
        Q(participante_1=otro_usuario, participante_2=request.user)
    ).first()
    
    if not conversacion:
        conversacion = Conversacion.objects.create(
            participante_1=request.user,
            participante_2=otro_usuario
        )
    
    return redirect('message_detail', conversation_id=conversacion.id)