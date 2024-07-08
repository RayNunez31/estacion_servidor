from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from estaciones.models import Newlectura as Lectura  # Ajusta el nombre del modelo según tu aplicación


def mediciones_list(request):
    datos = Lectura.objects.all().order_by('-hora')
    paginator = Paginator(datos, 10)  # Mostrar 10 elementos por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mediciones_list.html', {'page_obj': page_obj})


