from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from adm.models import Order, Settings, Status, Region, SecondaryBanner


class Show():
    def show_categories():
        categories = ['categoria1','categoria2','categoria3','categoria4','categoria5']
        return categories

    def show_status_color(pk):
        status = Order.objects.get(pk=pk).status.id
        if status == 1: #Pendiente de Pago
            badge = 'warning'
        elif status == 2: #Pagado
            badge = 'success'
        else:
            badge = 'primary'
        return badge

    def settings_data():
        try:
            Status.objects.get(pk=1)
        except Status.DoesNotExist:
            Status.objects.create(name='Pendiente de Pago')
            Status.objects.create(name='Pagado')
            Status.objects.create(name='Preparando el Pedido')
            Status.objects.create(name='Enviado')
            Status.objects.create(name='Pago Fallido')
            Status.objects.create(name='Reembolsado')
            Status.objects.create(name='En Revisión')
            Status.objects.create(name='Cliente Solicitó Reembolso')
            Status.objects.create(name='Cancelado')
            Status.objects.create(name='Banco Solicitó Reembolso')

        try:
            Region.objects.get(pk=2)
        except Region.DoesNotExist:
            Region.objects.create(name='Región de Arica y Parinacota')
            Region.objects.create(name='Región de Tarapacá')
            Region.objects.create(name='Región de Antofagasta')
            Region.objects.create(name='Región de Atacama')
            Region.objects.create(name='Región de Coquimbo')
            Region.objects.create(name='Región de Valparaíso')
            Region.objects.create(name='Región Metropolitana')
            Region.objects.create(name='Región Libertador General Bernardo O Higgins')
            Region.objects.create(name='Región del Maule')
            Region.objects.create(name='Región de Ñuble')
            Region.objects.create(name='Región del Biobío')
            Region.objects.create(name='Región de La Araucanía')
            Region.objects.create(name='Región de Los Ríos')
            Region.objects.create(name='Región de Los Lagos')
            Region.objects.create(name='Región de Aysén del General Carlos Ibáñez del Campo')
            Region.objects.create(name='Región de Magallanes y de la Antártica Chilena')

        try:
            SecondaryBanner.objects.get(pk=1)
        except SecondaryBanner.DoesNotExist:
            SecondaryBanner.objects.create(
                    name = 'Anuncio 1',
                    uploadedFile = "settings/logo.png"
            )
            SecondaryBanner.objects.create(
                    name = 'Anuncio 2',
                    uploadedFile = "settings/logo.png"
            )


        try:
            data = Settings.objects.get(pk=1)
        except:
            data = ''
        return data