from django import forms
from .models import Banner

class AddNewBanner(forms.ModelForm):

    class Meta:
        model = Banner

        fields = ['name','uploadedFile']
        labels = {
            'name': 'Ingresa un nombre para el Banner',
            'uploadedFile': 'Selecciona un Archivo'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'uploadedFile': forms.FileInput(attrs={'class':'form-control','accept':'image/png'})
        }