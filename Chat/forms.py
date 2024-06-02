from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    # QUITAR TEXTOS DE AYUDA
    username = forms.CharField(max_length=100, help_text='', widget=forms.TextInput(attrs={
        "placeholder": "pepito perez"
    }))
    password1 = forms.CharField(max_length=100, help_text='', widget=forms.PasswordInput(attrs={
        "placeholder": "password secret"
    }), label='password')
    password2 = forms.CharField(max_length=100, help_text='', widget=forms.PasswordInput(attrs={
        "placeholder": "confirm password secret"
    }), label='confirm password'
        )
    
    class Meta:
        model = User
        fields = ('email', 'username')
        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": "MyEmail@some.com"
            }),
        }
    
    # PONER CLASE FORM-CONTROL A TODOS LOS INPUTS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            