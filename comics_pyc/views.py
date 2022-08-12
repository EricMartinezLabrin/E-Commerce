from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic import DetailView,ListView,CreateView
from django.shortcuts import render
from django.contrib.auth.models import User

#local
from .functions import Show
from adm.models import Banner, Category, Product, Order,UserDetail
from .cart import CartProcessor
from adm import forms

def CreateUser(request):
    if request.method == 'POST':
        form_user = forms.CreateUser(request.POST)
        form_detail = forms.CreateUserDetail(request.POST)

        if form_user.is_valid():
            #User
            password = form_user.cleaned_data['password']
            username = form_user.cleaned_data['username']
            first_name = form_user.cleaned_data['first_name']
            last_name = form_user.cleaned_data['last_name']
            email = form_user.cleaned_data['email']

            if form_detail.is_valid():
                #UserDetail
                adress = form_detail.cleaned_data['adress']
                interior_number =  form_detail.cleaned_data['interior_number']
                comuna = form_detail.cleaned_data['comuna']
                region = form_detail.cleaned_data['region']
                phone = form_detail.cleaned_data['phone']

                user = User.objects.create_user(username,email,password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                userdetail = UserDetail.objects.create(user=user.id)
                userdetail.adress = adress
                userdetail.interior_number = interior_number
                userdetail.comuna = comuna
                userdetail.region = region
                userdetail.phone = phone
                userdetail.save()

                return HttpResponseRedirect(reverse("successfully"))
        else:
            return HttpResponseRedirect(reverse("failed"))
    else:
        return HttpResponse("No llega el formulario")

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
        return context
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = IndexView.show_product()
    #     return context

class DetailView(DetailView):
    template_name = 'inicio/details.html'
    model = Product

class CartView(TemplateView):
    template_name = 'inicio/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = IndexView.show_category()
        return context
    
        

class CheckoutView(TemplateView):
    template_name = 'inicio/checkout.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = IndexView.show_category()
        return context

class SuccessfullyView(TemplateView):
    template_name = 'inicio/successfully.html'

class FailedView(TemplateView):
    template_name = 'inicio/failed.html'

class LoginView(TemplateView):
    template_name = 'inicio/login.html'

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