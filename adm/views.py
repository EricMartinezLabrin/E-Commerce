#Django
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView

#Local
from .models import Banner,Category
from .forms import AddNewBanner, AddCategory

class IndexView(TemplateView):
    template_name = 'adm/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AdsView(TemplateView):
    template_name = 'adm/ads.html'
    form = AddNewBanner
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=self.form
        return context

def UploadBanner(request):
    if request.method == "POST":
        # Fetching the form data
        uploadedFile = request.FILES["uploadedFile"]
        name = request.POST["name"]

        # Saving the information in the database
        document = Banner(
            name = name,
            uploadedFile = uploadedFile
        )
        document.save()

    return HttpResponseRedirect(reverse_lazy("adm:ads"))

class CategoryView(TemplateView):
    template_name = 'adm/category.html'
    form = AddCategory
    categories = Category.objects.filter(status=True)

    def find_categories():
        categories = Category.objects.all()
        return categories

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=self.form
        context['categories']=CategoryView.find_categories()
        return context

def Category_Create(request):
    if request.method == "POST":
        # Fetching the form data
        uploadedFile = request.FILES["banner"]
        name = request.POST["name"]

        # Saving the information in the database
        document = Category(
            name = name,
            banner = uploadedFile
        )
        document.save()

    return HttpResponseRedirect(reverse_lazy("adm:category"))

def CategoryBannerView(request):
     return render(request, 'adm/modal_preview_category.html')