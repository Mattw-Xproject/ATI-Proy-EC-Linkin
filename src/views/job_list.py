from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.db.models import Count, Q
from src.models import OfertaEmpleo, Postulacion

@login_required
def job_list(request):
    """
    Vista principal de empleos
    Diferente para profesionales vs empresas
    """
    user = request.user
    
    if user.tipo_usuario == 'profesional':
        # Vista para profesionales: Ver ofertas disponibles
        ofertas_destacadas = OfertaEmpleo.objects.filter(
            activa=True,
            destacada=True
        ).select_related('empresa__user')[:3]
        
        ofertas_recomendadas = OfertaEmpleo.objects.filter(
            activa=True
        ).exclude(
            id__in=[o.id for o in ofertas_destacadas]
        ).select_related('empresa__user').annotate(
            postulaciones_count=Count('postulaciones')
        )[:10]
        
        # Ofertas guardadas
        ofertas_guardadas = OfertaEmpleo.objects.filter(
            postulaciones__profesional=user.profesional,
            postulaciones__guardada=True
        ).select_related('empresa__user')
        
        context = {
            'ofertas_destacadas': ofertas_destacadas,
            'ofertas_recomendadas': ofertas_recomendadas,
            'ofertas_guardadas': ofertas_guardadas,
            'user_type': 'profesional',
        }
        
        return render(request, 'jobs/job_list_profesional.html', context)
    
    elif user.tipo_usuario == 'empresa':
        # Vista para empresas: Ver sus propias ofertas (activas E inactivas)
        ofertas_activas = user.empresa.ofertas.filter(
            activa=True
        ).annotate(
            postulaciones_count=Count('postulaciones')
        ).order_by('-fecha_publicacion')
        
        ofertas_inactivas = user.empresa.ofertas.filter(
            activa=False
        ).annotate(
            postulaciones_count=Count('postulaciones')
        ).order_by('-fecha_publicacion')
        
        # Estadísticas
        total_postulaciones = Postulacion.objects.filter(
            oferta__empresa=user.empresa
        ).count()
        
        context = {
            'ofertas_activas': ofertas_activas,
            'ofertas_inactivas': ofertas_inactivas,
            'total_postulaciones': total_postulaciones,
            'user_type': 'empresa',
        }
        
        return render(request, 'jobs/job_list_empresa.html', context)