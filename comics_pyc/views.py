from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import DetailView,ListView,CreateView
from django.shortcuts import render

#local
from .functions import Show
from adm.models import Banner, Category, Product, Order
from .cart import CartProcessor

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