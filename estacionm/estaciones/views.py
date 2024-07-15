from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from estaciones.models import Newlectura as Lectura  # Ajusta el nombre del modelo según tu aplicación
from estaciones.models import Estac
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import EstacForm
from django.contrib import messages


@login_required
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
def dashboard_estacion(request):
    return render(request, 'dashboard_estacion.html')