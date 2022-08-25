from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from adm.models import Order, Settings


class Show():
    def show_categories():
        categories = ['categoria1','categoria2','categoria3','categoria4','categoria5']
        return categories

    def show_status_color(pk):
        status = Order.objects.get(pk=pk).status.id
        if status == 1: #Pendiente de Pago
            badge = 'warning'
        if status == 2: #Pagado
            badge = 'success'
        return badge

    def settings_data():
        try:
            data = Settings.objects.get(pk=1)
        except:
            data = ''
        return data