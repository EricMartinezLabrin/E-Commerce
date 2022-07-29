from django import forms
from .models import Banner,Category,SubCategory

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

class AddCategory(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name','banner']
        labels = {
            'name': 'Ingresa un Nombre',
            'banner': 'Selecciona una imagen para el banner'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'banner': forms.FileInput(attrs={'class':'form-control', 'acept':'image/png'})
        }

class AddSubCategory(forms.ModelForm):

    class Meta:
        model = SubCategory
        fields = ['name','subcategory','banner']
        labels = {
            'name': 'Ingresa un Nombre',
            'subcategory': 'Selecciona Categoria Principal',
            'banner': 'Selecciona una imagen para el banner'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'subcategory': forms.Select(attrs={'class':'form-control'}),
            'banner': forms.FileInput(attrs={'class':'form-control', 'acept':'image/png'})
        }