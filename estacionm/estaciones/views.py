from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Medicionescombinadas

def mediclima_list(request):
    mediciones = Medicionescombinadas.objects.all().order_by('-fecha_lec_sen')
    paginator = Paginator(mediciones, 10)  # Mostrar 10 registros por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mediclima_list.html', {'page_obj': page_obj})