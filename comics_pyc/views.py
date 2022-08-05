#Django
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.shortcuts import render
from .functions import Show
from adm.models import Banner, Category, Product

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

class CheckoutView(TemplateView):
    template_name = 'inicio/checkout.html'

class LoginView(TemplateView):
    template_name = 'inicio/login.html'