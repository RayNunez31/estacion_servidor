from django import forms
from .models import Estac, Sensor

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