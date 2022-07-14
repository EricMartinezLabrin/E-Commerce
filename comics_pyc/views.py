#Django
from pipes import Template
from django.views.generic.base import TemplateView
from django.shortcuts import render
from .functions import Show

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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