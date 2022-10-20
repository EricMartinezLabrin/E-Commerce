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
from .functions import GetData, Show
from adm.models import Banner, Category, Product, Order, SecondaryBanner, Settings, SubCategory,UserDetail, Status,Cart,Parcel, Why
from .cart import CartProcessor
from adm import forms
from .credentials import Credentials

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

    def show_secondary_banner(active=True):
        show = SecondaryBanner.objects.filter(status=active)
        return show

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banner'] = IndexView.show_banner()
        context['categories'] = IndexView.show_category()
        context['products'] = IndexView.show_product()
        context['data_settings'] = Show.settings_data()
        context['secondary_banner'] = IndexView.show_secondary_banner()
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

    def show_subcategories(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        subcateries = SubCategory.objects.filter(category=category)
        return subcateries

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.show_products()
        context['categories'] = IndexView.show_category()
        context['data_settings'] = Show.settings_data()
        context['subcategory'] = self.show_subcategories()
        return context

def SubcategoryView(request,pk):
    template_name='inicio/subcategory.html'
    subcategory=SubCategory.objects.get(pk=pk)
    products = Product.objects.filter(subcategory=subcategory)
    return render(request,template_name,{
        'products':products,
        'data_settings' : Show.settings_data(),
        'categories' : IndexView.show_category(),
        'object':subcategory
    })
    
class DetailView(DetailView):
    template_name = 'inicio/details.html'
    model = Product

    def get_why():
        why = Why.objects.all()
        return why
    
    def best_seller_data(self):
        best = GetData.get_bestseller()

        if str(best[0][0]) == str(self.kwargs.get('pk')):
            best_data = best[1][0]
        else:
            best_data = best[0][0]
        p=Product.objects.get(pk=best_data)
        data_export={
            'name':p.name,
            'price':p.price,
            'description':p.description,
            'image':p.image,
            'id':p.id
        }
        return data_export    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = IndexView.show_category()
        context['data_settings'] = Show.settings_data()
        context['why'] = DetailView.get_why()
        context['best_seller'] = self.best_seller_data()
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
    order = None

    if cart_data is not {}:
        template_name = 'inicio/processing.html'
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
        #CREATE ITEMS
        items =[]
        for key, value in cart_data.items():
            # for key, value in value.items():
            block = {
                "id": str(value['product_id']),
                "title": value['name'],
                "currency_id": "CLP",
                "picture_url": "/media"+value['image'],
                "description": value['description'],
                "quantity": value['quantity'],
                "unit_price": Product.objects.get(pk=value['product_id']).price
            }
            items.append(block)

        # Agrega credenciales
        sdk = mercadopago.SDK(Credentials.mercadopago())


        # Crea un ítem en la preferencia
        preference_data = {
            "items": items,

        "payer": {
            "name": request.user.first_name,
            "surname": request.user.last_name,
            "email": request.user.email,
            "phone": {
                "area_code": "56",
                "number": request.user.userdetail.phone
                    }
                },
        "back_urls": {
            "success": Credentials.success_url(),
            "failure": Credentials.failure_url(),
            "pending": Credentials.pending_url()
        },
        "auto_return": "approved",
        "notification_url":Credentials.notification_url(),
        "statement_descriptor": "IKIGAIMANGA",
        "external_reference": str(order_id.id),
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        return render(request,template_name,{
        'order': order_id,
        'data_settings': Show.settings_data(),
        'preference': preference,
        'credentials': Credentials.mercadopago()
    })

def SuccessfullyView(request):
    template_name = 'inicio/successfully.html'
    data_settings = Show.settings_data()
    merchant_order_id = request.GET['merchant_order_id']
    payment_type = request.GET['payment_type']
    status = request.GET['status']
    external_reference = request.GET['external_reference']
    
    return render(request,template_name,{
        'merchant_order_id': merchant_order_id,
        'payment_type': payment_type,
        'status': status,
        'external_reference': external_reference,
        'data_settings':data_settings
    })

def FailedView(request):
    template_name = 'inicio/failed.html'
    data_settings = Show.settings_data()
    merchant_order_id = request.GET['merchant_order_id']
    payment_type = request.GET['payment_type']
    status = request.GET['status']
    external_reference = request.GET['external_reference']
    
    return render(request,template_name,{
        'merchant_order_id': merchant_order_id,
        'payment_type': payment_type,
        'status': status,
        'external_reference': external_reference,
        'data_settings':data_settings
    })

def PendingView(request):
    template_name = 'inicio/pending.html'
    data_settings = Show.settings_data()
    merchant_order_id = request.GET['merchant_order_id']
    payment_type = request.GET['payment_type']
    status = request.GET['status']
    external_reference = request.GET['external_reference']
    
    return render(request,template_name,{
        'merchant_order_id': merchant_order_id,
        'payment_type': payment_type,
        'status': status,
        'external_reference': external_reference,
        'data_settings':data_settings
    })

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
        object_list = Order.objects.filter(customer=customer).order_by('-id')
    except Order.DoesNotExist:
        object_list = None

    return render(request,template_name,{
        'object_list':object_list,
        'data_settings':data_settings
    })

class ContactView(DetailView):
    model = Settings
    template_name = 'inicio/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = IndexView.show_category()
        context['data_settings'] = Show.settings_data()
        return context 

class TyCView(TemplateView):
    template_name = "inicio/tyc.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = IndexView.show_category()
        context['data_settings'] = Show.settings_data()
        return context 



    
