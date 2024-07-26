from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from estaciones.models import Newlectura as Lectura  # Ajusta el nombre del modelo según tu aplicación
from estaciones.models import Estac
from estaciones.models import Sensor
from estaciones.models import Alarmas
from estaciones.models import Notificaciones
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import AlarmaForm, EstacForm, SensorForm
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist
from .forms import EstacUpdateForm
from .forms import CustomUserCreationForm
from datetime import datetime
from django.db.models import Q



@login_required
def eliminar_cuenta(request):
    # Lógica para eliminar la cuenta del usuario actual
    request.user.delete()  # Borra el usuario actual
    
    logout(request)  # Cierra la sesión del usuario
    
    return redirect('/login/')  # Redirige a la página de inicio de sesión

@login_required
def user_account_view(request):
    # Obtenemos el usuario autenticado
    user = request.user

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Los datos han sido actualizados exitosamente')
        # Puedes agregar un mensaje de éxito aquí si lo deseas
        return redirect('/UserAccount')
    
    
    
    context = {
        'user': user  # Pasamos el objeto user a la plantilla
    }
    return render(request, 'user_account.html', context)


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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
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
    lecturas_estacion = Lectura.objects.filter(estacion=estacion)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            # Eliminar lecturas relacionadas específicamente a esta estación
            lecturas_estacion.delete()
            # Eliminar sensores relacionados específicamente a esta estación
            sensores_estacion.delete()
            # Eliminar la estación
            estacion.delete()
            #messages.success(request, 'La estación y todas sus lecturas y sensores relacionados han sido eliminados exitosamente.')
            return redirect('/')  # Actualiza esto con la vista a la que deseas redirigir
        
        elif 'delete-sensor' in request.POST:
            sensor_id = request.POST.get('sensor_id')
            sensor = get_object_or_404(Sensor, id_sensor=sensor_id)
            sensor.delete()
            #messages.success(request, 'El sensor ha sido eliminado exitosamente.')
            return redirect('/')
        else:
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
def agregar_sensor_view(request):
    estacion_id = request.GET.get('estacion_id')

    estacion = get_object_or_404(Estac, id_estacion=estacion_id)
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Se ha agregado correctamente el sensor a la estacion')
        sensor = form.save(commit=False)
        sensor.estacion = estacion
        sensor.save()
            
    else:
        form = SensorForm()


    context = {
        'estacion': estacion,
        'form': form,
    }
    return render(request, 'agregar_sensor.html', context)

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
def alarmas_view(request):
    estacion_id = request.GET.get('estacion_id')
    estacion = get_object_or_404(Estac, id_estacion=estacion_id)
    alarmas = Alarmas.objects.filter(estacion=estacion)

    paginator = Paginator(alarmas, 4)  # Muestra 10 alarmas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        if 'save' in request.POST:
            form = AlarmaForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Se ha agregado correctamente la alarma a la estación')
                alarma = form.save(commit=False)
                alarma.estacion = estacion
                alarma.save()
        elif 'delete-alarm' in request.POST:
            alarma_id = request.POST.get('alarma_id')
            alarma = get_object_or_404(Alarmas, id_alarma=alarma_id)  # Ajustar a tu modelo de Alarma
            alarma.delete()

    else:
        form = AlarmaForm()

    context = {
        'alarmas': page_obj.object_list,
        'page_obj': page_obj,
        'estacion': estacion,
    }
    return render(request, 'alarmas.html', context)

@login_required
def registro_lectura_view(request):
    estacion_id = request.GET.get('estacion_id')
    query = request.GET.get('q', '')
    estacion = get_object_or_404(Estac, id_estacion=estacion_id)

    if estacion_id:
        lecturas = Lectura.objects.filter(estacion=estacion)
        if query:
            try:
                # Convertir el formato de la consulta en un objeto datetime
                fecha_hora = datetime.fromisoformat(query)
                fecha = fecha_hora.date()
                hora = fecha_hora.time()
                
                # Filtrar por fecha y hora
                lecturas = lecturas.filter(
                    Q(hora__date=fecha) & 
                    Q(hora__time__hour=hora.hour) & 
                    Q(hora__time__minute=hora.minute)
                )
            except ValueError:
                # Manejar el caso donde el formato de la fecha y hora es incorrecto
                lecturas = Lectura.objects.none()
    else:
        lecturas = Lectura.objects.none()

    paginator = Paginator(lecturas, 10)  # Mostrar 10 lecturas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'estacion': estacion,  # Reemplaza con los datos reales de la estación
    }
    return render(request, 'registro_lectura.html', context)