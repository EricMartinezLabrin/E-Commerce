from django.db import models
from django.contrib.auth.models import User

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
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True)
    price = models.IntegerField()
    description = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    image = models.FileField(upload_to="products/")

    def __str__(self):
        return self.name
