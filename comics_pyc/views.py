#Django
from django.views.generic.base import TemplateView
from django.shortcuts import render
from .functions import Show
from adm.models import Banner

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

    def show_banner(self):
        banner = Banner.objects.all()
        return banner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banner'] = IndexView.show_banner(self)
        context['categories'] = Show.show_categories()
        context['products'] = IndexView.show_products(self)
        return context

class CategoriesView(TemplateView):
    template_name = 'inicio/categorie.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = IndexView.show_products(self)
        return context

class DetailView(TemplateView):
    template_name = 'inicio/details.html'

class CartView(TemplateView):
    template_name = 'inicio/cart.html'

class CheckoutView(TemplateView):
    template_name = 'inicio/checkout.html'

class LoginView(TemplateView):
    template_name = 'inicio/login.html'