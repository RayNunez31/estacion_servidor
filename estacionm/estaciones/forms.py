from django import forms
from .models import Estac, Sensor, Alarmas
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254,)
    first_name = forms.CharField(max_length=30, )
    last_name = forms.CharField(max_length=30, )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class EstacForm(forms.ModelForm):

    class Meta:
        model = Estac
        fields = [ 'nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'descripcion': forms.Textarea(attrs={'required': True}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        # Validación para asegurarse de que nombre no esté duplicado
        if Estac.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("Ya existe una estación con este nombre.")

        return nombre
    
class EstacUpdateForm(forms.ModelForm):
    class Meta:
        model = Estac
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'descripcion': forms.Textarea(attrs={'required': True}),
        }
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        # Validación para asegurarse de que nombre no esté duplicado
        if Estac.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("Ya existe una estación con este nombre.")

        return nombre

class SensorForm(forms.ModelForm):

    class Meta:
        model = Sensor
        fields = ['nombre', 'modelo', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'modelo': forms.TextInput(attrs={'required': True}),
            'descripcion': forms.Textarea(attrs={'required': False}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        estacion = self.cleaned_data.get('estacion')

        # Validación para asegurarse de que nombre no esté duplicado para la misma estación
        if Sensor.objects.filter(nombre=nombre, estacion=estacion).exists():
            raise forms.ValidationError("Ya existe un sensor con este nombre para esta estación.")

        return nombre
    
class AlarmaForm(forms.ModelForm):
    class Meta:
        model = Alarmas
        fields = ['nombre', 'descripcion', 'temperatura', 'humedad', 'presionatmosferica', 'velocidad_del_viento', 'pluvialidad']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),
            'temperatura': forms.NumberInput(attrs={'min': -20, 'max': 50, 'step': 0.01}),
            'humedad': forms.NumberInput(attrs={'min': 5, 'max': 30, 'step': 0.01}),
            'presionatmosferica': forms.NumberInput(attrs={'min': 980, 'max': 1050, 'step': 0.01}),
            'velocidad_del_viento': forms.NumberInput(attrs={'min': 0, 'max': 60, 'step': 0.01}),
            'pluvialidad': forms.NumberInput(attrs={'min': 0, 'max': 150, 'step': 0.01}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        estacion = self.cleaned_data.get('estacion')

        # Validación para asegurarse de que nombre no esté duplicado para la misma estación
        if Alarmas.objects.filter(nombre=nombre, estacion=estacion).exists():
            raise forms.ValidationError("Ya existe una alarma con este nombre para esta estación.")

        return nombre