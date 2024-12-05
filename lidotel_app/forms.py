from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reserva

class AgenciaRegistroForm(UserCreationForm):
    nombre_agencia = forms.CharField(max_length=100)
    direccion = forms.CharField(widget=forms.Textarea)
    telefono = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'nombre_agencia', 'direccion', 'telefono')

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        exclude = ('agencia', 'puntos_generados', 'fecha_creacion', 'estado')
        widgets = {
            'fecha_checkin': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'placeholder': 'Fecha de Check-in'
            }),
            'fecha_checkout': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'placeholder': 'Fecha de Check-out'
            }),
            'tipo_habitacion': forms.Select(attrs={'class': 'form-control'}),
            'nombre_huesped': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del huésped'
            }),
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de documento'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'numero_habitaciones': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'numero_huespedes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'comentarios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Comentarios adicionales'
            }),
            'no_fumador': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vista_mar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acceso_discapacitados': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cama_adicional': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'transporte_aeropuerto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tours_locales': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'servicio_spa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        } 