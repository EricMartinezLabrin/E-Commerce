#Django
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import CreateView

#Local
from .models import Banner
from .forms import AddNewBanner

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

    documents = Banner.objects.all()

    return render(request, "adm/ads.html", context = {
        "files": documents
    })