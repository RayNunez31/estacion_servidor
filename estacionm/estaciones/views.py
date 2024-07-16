from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from estaciones.models import Newlectura as Lectura  # Ajusta el nombre del modelo según tu aplicación
from estaciones.models import Estac
from estaciones.models import Sensor
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import EstacForm
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist
from .forms import EstacUpdateForm




def mediciones_list(request):
    datos = Lectura.objects.all().order_by('-hora')
    paginator = Paginator(datos, 10)  # Mostrar 10 elementos por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mediciones_list.html', {'page_obj': page_obj})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Nombre de usuario o contraseña incorrectos'
    return render(request, 'login.html', {'error_message': error_message})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login/')

@login_required
def estaciones(request):
    estaciones_list = Estac.objects.all()

    # Ordenamiento por nombre (por defecto ascendente)
    sort = request.GET.get('sort', 'asc')
    if sort == 'desc':
        estaciones_list = estaciones_list.order_by('-nombre')
    else:
        estaciones_list = estaciones_list.order_by('nombre')

    # Búsqueda por nombre
    query = request.GET.get('q')
    if query:
        estaciones_list = estaciones_list.filter(nombre__icontains=query)

    # Paginación
    paginator = Paginator(estaciones_list, 5)  # 10 items por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sort': sort,
        'query': query,
    }
    return render(request, 'estaciones.html', context)

@login_required
def crear_estacion(request):
    if request.method == 'POST':
        form = EstacForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Se ha creado la estación correctamente.')
            form.save()
    else:
        form = EstacForm()
    
    return render(request, 'crear_estacion.html', {'form': form})

@login_required
def administrar_view(request):
    estacion_id = request.GET.get('estacion_id')
    estacion = get_object_or_404(Estac, id_estacion=estacion_id)
    sensores_estacion = Sensor.objects.filter(estacion=estacion)
    
    if request.method == 'POST':
        form = EstacUpdateForm(request.POST, instance=estacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los datos de la estación han sido actualizados correctamente.')
    else:
        form = EstacUpdateForm(instance=estacion)

    context = {
        'estacion': estacion,
        'sensores': sensores_estacion,
        'form': form,
    }
    return render(request, 'administrar_estaciones.html', context)

@login_required
def dashboard_view(request):
    estacion_id = request.GET.get('estacion_id')
    
    # Cargar datos de la estación usando estacion_id
    estacion = get_object_or_404(Estac, id_estacion=estacion_id)
    
    # Obtener la última lectura asociada a esta estación
    try:
        ultima_lectura = Lectura.objects.filter(estacion=estacion).latest('hora')
    except ObjectDoesNotExist:
        ultima_lectura = None

    sensores_estacion = Sensor.objects.filter(estacion=estacion)

    # Pasar 'estacion' y 'ultima_lectura' al contexto de renderizado de tu plantilla de dashboard
    context = {
        'estacion': estacion,
        'ultima_lectura': ultima_lectura,
        'sensores': sensores_estacion,
    }


    
    return render(request, 'dashboard_estacion.html', context)
@login_required
def lectura_detalle(request):
    lectura_id = request.GET.get('lectura_id')
    lectura = get_object_or_404(Lectura, id_lectura=lectura_id)

    context = {
        'lectura':lectura,
    }
    return render(request, 'lectura_detalle.html', context)

@login_required
def registro_lectura_view(request):
    estacion_id = request.GET.get('estacion_id')
    
    
    # Cargar datos de la estación usando estacion_id
    estacion = get_object_or_404(Estac, id_estacion=estacion_id)
    
    # Obtener las lecturas asociadas a esta estación
    lecturas_estacion = Lectura.objects.filter(estacion=estacion) 

    # Ordenamiento por hora (por defecto ascendente)
    sort = request.GET.get('sort', 'asc')
    if sort == 'desc':
        lecturas_estacion = lecturas_estacion.order_by('-hora')
    else:
        lecturas_estacion = lecturas_estacion.order_by('hora')

    # Búsqueda por fecha
    query = request.GET.get('q')
    if query:
        query_date = parse_date(query)
        if query_date:
            lecturas_estacion = lecturas_estacion.filter(hora__date=query_date)

    # Paginación
    paginator = Paginator(lecturas_estacion, 10)  # 10 items por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pasar 'estacion' y 'lecturas' al contexto de renderizado de tu plantilla de dashboard
    context = {
        'estacion': estacion,
        'lecturas': lecturas_estacion,
        'page_obj': page_obj,
        'sort': sort,
        'query': query,
    }
    
    return render(request, 'registro_lectura.html', context)

