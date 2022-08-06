from django.contrib import admin
from .models import Cart, Status, Region, UserDetail
# Register your models here.
admin.site.register(Cart)
admin.site.register(Status)
admin.site.register(Region)
admin.site.register(UserDetail)

class UserDetailInline(admin.StackedInline):
    model = UserDetail
    extra = 3
    fields = ['phone']