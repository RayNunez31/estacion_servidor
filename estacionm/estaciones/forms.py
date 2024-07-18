from django import forms
from .models import Estac, Sensor
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