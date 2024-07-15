from django import forms
from .models import Estac

class EstacForm(forms.ModelForm):
    id_estacion = forms.IntegerField(label='ID de Estación', disabled=False)

    class Meta:
        model = Estac
        fields = ['id_estacion', 'nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'descripcion': forms.TextInput(attrs={'required': True}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        # Validación para asegurarse de que nombre no esté duplicado
        if Estac.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("Ya existe una estación con este nombre.")

        return nombre