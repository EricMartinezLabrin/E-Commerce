from django.contrib import admin
from .models import Cart, Status, Region, UserDetail, Order
# Register your models here.
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Status)
admin.site.register(Region)
admin.site.register(UserDetail)