from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import DetailView,ListView,CreateView, UpdateView
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate, login

#local
from .functions import Show
from adm.models import Banner, Category, Product, Order,UserDetail, Status,Cart,Parcel
from .cart import CartProcessor
from adm import forms

#Otro
import mercadopago

def CreateUser(request):
    form = forms.CreateUser(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            #Create User       
            form.save()
            #Authenticate User
            username= form.cleaned_data['username']
            password= form.cleaned_data['password2']
            user = authenticate(username=username, password=password)

            if user is not None:
                #CreateUser
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                return HttpResponseRedirect(reverse("login"))
        else:
            return HttpResponse("No hemos recibido información, porfavor contactate con el administrador. (Formulario no Válido)")
    else:
        return render(request,'inicio/register.html',{
            'form': form,
            'data_settings': Show.settings_data()
        })

class LoginView(LoginView):
    template_name = 'inicio/login.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class Logout(LogoutView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class IndexView(TemplateView):
    template_name = 'inicio/index.html'

    def show_products(self):
        quantity = 10
        counter = 0
        products = []
        for i in range(0,quantity):
            counter+=1
            products.append(f"Producto {counter}")
        return products

    def show_banner(active=True):
        banner = Banner.objects.filter(status=active)
        return banner

    def show_category(active=True):
        show = Category.objects.filter(status=active)
        return show

    def show_product(active=True):
        show = Product.objects.filter(status=active)
        return show

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banner'] = IndexView.show_banner()
        context['categories'] = IndexView.show_category()
        context['products'] = IndexView.show_product()
        context['data_settings'] = Show.settings_data()
        return context

class AllProductsView(ListView):
    template_name = 'inicio/all_products.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = IndexView.show_category()
        context['data_settings'] = Show.settings_data()
        return context

class CategoriesView(DetailView):
    template_name = 'inicio/categorie.html'
    model = Category
    
    def show_products(self):
        show_product = Product.objects.filter(category=self.kwargs['pk'])
        return show_product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.show_products()
        context['categories'] = IndexView.show_category()
        context['data_settings'] = Show.settings_data()
        return context

class DetailView(DetailView):
    template_name = 'inicio/details.html'
    model = Product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class CartView(TemplateView):
    template_name = 'inicio/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = IndexView.show_category()
        context['data_settings'] = Show.settings_data()
        return context
          
def CheckoutView(request):
    template_name = 'inicio/checkout.html'
    details = User.objects.get(pk=request.user.id)
    parcel = Parcel.objects.all()
    try:
        form = forms.CreateUserDetail(request.POST or None, instance=details.userdetail)
    except:
        form = forms.CreateUserDetail(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                user_details = UserDetail()
                user_details.phone = form.cleaned_data['phone']
                user_details.address = form.cleaned_data['address']
                user_details.interior_number = form.cleaned_data['interior_number']
                user_details.comuna = form.cleaned_data['comuna']
                user_details.region = form.cleaned_data['region']
                user_details.user = details
                user_details.save()
                return HttpResponseRedirect(reverse('payment'))
        return render(request,template_name,{
            'form_detail':form,
            'data_settings': Show.settings_data()
        })

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('payment'))
        else:
            return render(request,'inicio/failed.html',{
                'error': form,
                'data_settings': Show.settings_data()
            })
        

    return render(request,template_name,{
        'form_detail': form,
        'parcel': parcel,
        'data_settings': Show.settings_data()
    })

def paymentView(request):
    cart_data = request.session.get('cart_number')

    if cart_data is not {}:
        template_name = 'inicio/successfully.html'
        order = Order()
        subtotal = request.session.get('cart_total')
        total_shipping = 0

        #Order
        order.num_items_sold = request.session.get('cart_quantity')
        order.subtotal = subtotal
        order.total_shipping = total_shipping
        order.total = int(subtotal)+int(total_shipping)
        order.customer = request.user
        order.status = Status.objects.get(pk=1)
        order.save()

        #Cart
        for key,value in cart_data.items():
            order_id = Order.objects.filter(customer=request.user, status=Status.objects.get(pk=1)).last()
            product = Product.objects.get(pk=value['product_id'])
            quantity = value['quantity']
            subtotal = value['price']
            Cart.objects.create(order=order_id,product=product,quantity=quantity,subtotal=subtotal)

        request.session['cart_number']={}
        request.session['cart_total'] = 0
        request.session['cart_quantity'] = 0
        request.session.modified=True

        # SDK de Mercado Pago

        # Agrega credenciales
        sdk = mercadopago.SDK("TEST-1816279427628496-082518-84255c0be73596985adaf2dccacaeee1-113262566")


        # Crea un ítem en la preferencia
        preference_data = {
            "items": [
                {
                    "title": "Mi producto",
                    "quantity": 1,
                    "unit_price": 75
                }
            ]
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return render(request,template_name,{
        'order': order_id,
        'data_settings': Show.settings_data(),
        'preference': preference
    })

class SuccessfullyView(TemplateView):
    template_name = 'inicio/successfully.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class FailedView(TemplateView):
    template_name = 'inicio/failed.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

def addCart(request,product_id):
    cart = CartProcessor(request)
    product = Product.objects.get(pk=product_id)
    cart.add(product)  
    return HttpResponseRedirect(reverse("cart"))

def removeCart(request,product_id):
    cart = CartProcessor(request)
    product = Product.objects.get(pk=product_id)
    cart.remove(product)  
    return HttpResponseRedirect(reverse("cart"))

def decrementCart(request,product_id):
    cart = CartProcessor(request)
    product = Product.objects.get(pk=product_id)
    cart.decrement(product)  
    return HttpResponseRedirect(reverse("cart"))

def OrdersView(request,pk):
    model = Order
    template_name = 'inicio/orders.html'
    data_settings = Show.settings_data()
    customer = User.objects.get(pk=pk)

    try:
        object_list = Order.objects.filter(customer=customer)
    except Order.DoesNotExist:
        object_list = None

    return render(request,template_name,{
        'object_list':object_list,
        'data_settings':data_settings
    })

