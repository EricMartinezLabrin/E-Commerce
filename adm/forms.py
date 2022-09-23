#Django
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#Local
from .models import Banner,Category,SubCategory,Product,UserDetail, Parcel, Order, Settings, SecondaryBanner, Why


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

class SecondaryBannerForm(forms.ModelForm):

    class Meta:
        model = SecondaryBanner
        fields = ['name','uploadedFile']
        labels = {
            'name': 'Nombre',
            'uploadedFile': 'Nuevo Banner'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'uploadedFile': forms.FileInput(attrs={'class':'form-control'})
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
        fields = ['name','category','banner']
        labels = {
            'name': 'Ingresa un Nombre',
            'category': 'Selecciona Categoria Principal',
            'banner': 'Selecciona una imagen para el banner'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'banner': forms.FileInput(attrs={'class':'form-control', 'acept':'image/png'})
        }

class AddProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'name': 'Ingresa un Nombre',
            'category': 'Selecciona Categoria Principal',
            'subcategory': 'Selecciona una Categoria Secundaria',
            'price': 'Precio',
            'description': 'Escribe una descipción del producto',
            'image': 'Selecciona la imagen principal'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'subcategory': forms.Select(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control', 'acept':'image/png'})
        }

class CreateUser(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']

class CreateUser2(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2','is_staff']

        widgets = {
            'email':forms.TextInput(attrs={'class':'form-control m-2'}),
            'username':forms.TextInput(attrs={'class':'form-control m-2'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control m-2'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control m-2'})
        }

class CreateUserDetail(forms.ModelForm):

    class Meta:
        model = UserDetail
        fields = ['phone','address','interior_number','comuna','region','parcel']
        widgets = {
            'phone': forms.NumberInput(attrs={'class':'form-control','id':'phone'}),
            'address': forms.TextInput(attrs={'class':'form-control','id':'address'}),
            'interior_number': forms.NumberInput(attrs={'class':'form-control','id':'address2'}),
            'comuna': forms.TextInput(attrs={'class':'form-control','id':'comuna'}),
            'region': forms.Select(attrs={'class':'form-control','id':'state'}),
            'parcel': forms.RadioSelect(attrs={'id':'parcel'})
        }

class CreateParcel(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['name','min_price','max_price','image']
        labels = {
            'name': 'Nombre de Paqueteria',
            'min_price': 'Precio Mínimo',
            'max_price': 'Precio Máximo',
            'image': 'Logo de Paqueteria'
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control', 'acept':'image/png'}),
            'max_price':forms.NumberInput(attrs={'class':'form-control'}),
            'min_price':forms.NumberInput(attrs={'class':'form-control'})
        }

class OrderStatus(forms.ModelForm):
    class Meta:
        model= Order
        fields = ['status']
        labels = {
            'Status'
            }
        widget = {
            'status': forms.Select(attrs={'class':'form-control'})
        }

class SettingsForm(forms.ModelForm):
    class Meta:
        model= Settings
        fields = '__all__'
        labels = {
            'name': 'Nombre de la Empresa',
            'address': 'Dirección Empresa',
            'phone': 'Teléfono Empresa',
            'email': 'E-Mail Empresa',
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'logo': 'Logotipo'
        }
        widgets={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'facebook': forms.TextInput(attrs={'class':'form-control'}),
            'instagram': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.NumberInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'logo': forms.FileInput(attrs={'class':'form-control', 'acept':'image/png'})
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets={
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'})
        }

class ProfileDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['phone','address','interior_number','comuna','region','parcel','image']
        widgets = {
            'phone': forms.NumberInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'interior_number': forms.NumberInput(attrs={'class':'form-control'}),
            'comuna': forms.TextInput(attrs={'class':'form-control'}),
            'region': forms.Select(attrs={'class':'form-control'}),
            'parcel':forms.Select(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control', 'acept':'image/png'})
        }

class WhyForm(forms.ModelForm):
    class Meta:
        model = Why
        fields = ['name']
        labels = {
            'name': '¿Por qué comprar?'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'})
        }


