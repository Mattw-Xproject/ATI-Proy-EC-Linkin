from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q
from src.models import OfertaEmpleo, Postulacion

@login_required
def job_detail(request, job_id):
    """
    Vista de detalle de una oferta de empleo
    """
    oferta = get_object_or_404(
        OfertaEmpleo.objects.select_related('empresa__user'),
        id=job_id,
        activa=True
    )
    
    # Incrementar vistas
    oferta.vistas += 1
    oferta.save(update_fields=['vistas'])
    
    # Verificar si el usuario ya postuló
    ya_postulo = False
    guardada = False
    
    if request.user.tipo_usuario == 'profesional':
        try:
            postulacion = Postulacion.objects.get(
                profesional=request.user.profesional,
                oferta=oferta
            )
            ya_postulo = True
            guardada = postulacion.guardada
        except Postulacion.DoesNotExist:
            pass
    
    # Ofertas similares (misma empresa o mismo nivel)
    ofertas_similares = OfertaEmpleo.objects.filter(
        Q(empresa=oferta.empresa) | Q(nivel=oferta.nivel),
        activa=True
    ).exclude(
        id=oferta.id
    ).select_related('empresa__user')[:5]
    
    context = {
        'oferta': oferta,
        'ya_postulo': ya_postulo,
        'guardada': guardada,
        'ofertas_similares': ofertas_similares,
    }
    
    return render(request, 'jobs/job_detail.html', context)