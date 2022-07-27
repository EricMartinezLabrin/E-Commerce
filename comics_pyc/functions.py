from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class Show():
    def show_categories():
        categories = ['categoria1','categoria2','categoria3','categoria4','categoria5']
        return categories