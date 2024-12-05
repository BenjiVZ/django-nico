from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from .models import Agencia, Reserva, TipoHabitacion
from .forms import AgenciaRegistroForm, ReservaForm
from django.db.models import Sum, Count, Avg, Max
from django.contrib.admin.views.decorators import staff_member_required
import json

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {
        'total_agencias': Agencia.objects.count(),
        'total_reservas': Reserva.objects.count(),
        'total_puntos': Agencia.objects.aggregate(Sum('puntos_actuales'))['puntos_actuales__sum'] or 0
    }
    return render(request, 'index.html', context)

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = AgenciaRegistroForm()
    return render(request, 'auth.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Credenciales inválidas'})
    return redirect('auth')

def registro_usuario(request):
    if request.method == 'POST':
        form = AgenciaRegistroForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    # Crear la agencia asociada
                    Agencia.objects.create(
                        usuario=user,
                        nombre_agencia=form.cleaned_data['nombre_agencia'],
                        direccion=form.cleaned_data['direccion'],
                        telefono=form.cleaned_data['telefono']
                    )
                    login(request, user)
                    return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)})
        return JsonResponse({'success': False, 'errors': form.errors})
    return redirect('auth')

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
        
    # Verificar si el usuario tiene una agencia asociada
    try:
        agencia = request.user.agencia
    except Agencia.DoesNotExist:
        # Si no tiene agencia, crear una por defecto
        agencia = Agencia.objects.create(
            usuario=request.user,
            nombre_agencia=f"Agencia de {request.user.username}",
            direccion="Por definir",
            telefono="Por definir"
        )

    tipos_habitacion = TipoHabitacion.objects.all()
    
    # Obtener reservas de los últimos 30 días
    fecha_limite = timezone.now() - timedelta(days=30)
    reservas = Reserva.objects.filter(
        agencia=agencia,
        fecha_creacion__gte=fecha_limite
    ).order_by('-fecha_creacion')

    context = {
        'agencia': agencia,
        'tipos_habitacion': tipos_habitacion,
        'reservas': reservas,
        'form': ReservaForm()
    }
    return render(request, 'dashboard.html', context)

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.agencia = request.user.agencia
            reserva.save()
            return JsonResponse({
                'success': True,
                'puntos_generados': reserva.puntos_generados,
                'puntos_totales': request.user.agencia.puntos_actuales
            })
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = [str(error) for error in error_list]
        return JsonResponse({
            'success': False,
            'errors': errors
        })

@login_required
def editar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, agencia=request.user.agencia)
    
    # Verificar si la reserva tiene menos de 30 días
    if timezone.now() - reserva.fecha_creacion > timedelta(days=30):
        return JsonResponse({'success': False, 'error': 'No se puede editar una reserva con más de 30 días'})
    
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    # Si es GET, devolver el formulario HTML
    form = ReservaForm(instance=reserva)
    return render(request, 'reserva_form.html', {'form': form})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('index')

@staff_member_required
def admin_dashboard(request):
    # Estadísticas generales
    stats = {
        'total_puntos': Agencia.objects.aggregate(Sum('puntos_actuales'))['puntos_actuales__sum'] or 0,
        'total_agencias': Agencia.objects.count(),
        'total_reservas': Reserva.objects.count(),
        'reservas_recientes': Reserva.objects.count(),
    }
    
    # Últimas agencias
    agencias = Agencia.objects.annotate(
        ultima_actividad=Max('reserva__fecha_creacion'),
        total_reservas=Count('reserva')
    ).order_by('-ultima_actividad')[:10]
    
    # Reservas recientes
    reservas_recientes = Reserva.objects.select_related(
        'agencia', 'tipo_habitacion'
    ).order_by('-fecha_creacion')[:10]
    
    # Datos para gráficos
    reservas_por_tipo = (Reserva.objects
        .values('tipo_habitacion__nombre')
        .annotate(total=Count('id'))
        .order_by('-total'))
    
    puntos_por_agencia = (Agencia.objects
        .values('nombre_agencia')
        .annotate(puntos=Sum('puntos_actuales'))
        .order_by('-puntos')[:5])
    
    context = {
        'stats': stats,
        'agencias': agencias,
        'reservas_recientes': reservas_recientes,
        'chart_data': {
            'reservas_por_tipo': json.dumps(list(reservas_por_tipo)),
            'puntos_por_agencia': json.dumps(list(puntos_por_agencia)),
        }
    }
    return render(request, 'admin_dashboard.html', context)
