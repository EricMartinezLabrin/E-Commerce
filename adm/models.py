from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField

class Region(models.Model):
    name = models.CharField(max_length=51)

    def __str__(self):
        return self.name

class Parcel(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to="parcel/")
    max_price = models.IntegerField()
    min_price = models.IntegerField()

    def __str__(self):
        return self.name

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=250)
    interior_number = models.IntegerField()
    comuna = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, null=True)
    image = models.FileField(upload_to="profile/", null=True, blank=True)

    def __str__(self):
        return self.user.username

class Banner(models.Model):
    name = models.CharField(max_length=50,unique=True)
    uploadedFile = models.FileField(upload_to = "banner/")
    status = models.BooleanField(default=True)
    dateTimeOfUpload = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=30,unique=True)
    banner = models.FileField(upload_to="categories/")
    status = models.BooleanField(default=True)
    description = models.CharField(max_length=255,blank=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=30,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    banner = models.FileField(upload_to="subcategories/")
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField()
    description = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    image = models.FileField(upload_to="products/")

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Tax(models.Model):
    name = models.CharField(max_length=10)
    tax = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model):
    creation_date = models.DateTimeField(auto_now=True)
    num_items_sold = models.IntegerField()
    subtotal = models.IntegerField()
    total_shipping = models.IntegerField()
    total = models.IntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.CASCADE)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.IntegerField()
    creation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order)

class Settings(models.Model):
    name = models.CharField(default='My Business', max_length=50)
    address = models.CharField(default='My Address', max_length=255)
    phone = models.IntegerField(default=0)
    email = models.EmailField(default='contacto@mybusiness.com')
    logo = models.FileField(upload_to="settings/")

    def __str__(self):
        return self.name

