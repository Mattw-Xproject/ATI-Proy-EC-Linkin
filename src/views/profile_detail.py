from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from src.models import Usuario, Profesional, Empresa

@login_required
def profile_detail(request, user_id):
    """
    Vista de detalle de perfil (Profesional o Empresa)
    Detecta automáticamente el tipo de usuario y muestra el template correspondiente
    """
    user = get_object_or_404(Usuario, id=user_id)
    is_own_profile = request.user.id == user_id
    
    context = {
        'profile_user': user,
        'is_own_profile': is_own_profile,
    }
    
    # Determinar tipo de perfil y cargar datos específicos
    if user.tipo_usuario == 'profesional':
        try:
            profesional = user.profesional
            context['profesional'] = profesional
            context['habilidades'] = profesional.habilidades.all()[:10]  # Top 10 skills
            context['educaciones'] = profesional.educaciones.all()[:5]
            context['experiencias'] = profesional.experiencias.all()[:5]
            template = 'profiles/profesional_detail.html'
        except Profesional.DoesNotExist:
            # Si no existe el perfil, redirigir a completar
            from django.shortcuts import redirect
            from django.contrib import messages
            messages.warning(request, _('Por favor, completa tu perfil profesional'))
            return redirect('profile_edit', user_id=user_id)
    
    elif user.tipo_usuario == 'empresa':
        try:
            empresa = user.empresa
            context['empresa'] = empresa
            # Obtener ofertas publicadas por la empresa (cuando esté implementado)
            # context['ofertas'] = empresa.ofertas.filter(activa=True)[:5]
            template = 'profiles/empresa_detail.html'
        except Empresa.DoesNotExist:
            from django.shortcuts import redirect
            from django.contrib import messages
            messages.warning(request, _('Por favor, completa tu perfil de empresa'))
            return redirect('profile_edit', user_id=user_id)
    
    else:
        template = 'profiles/profile_detail.html'  # Template genérico fallback
    
    return render(request, template, context)