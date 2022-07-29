#django
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = "adm"
urlpatterns = [
    #extension: /adm/
    path("", views.IndexView.as_view(), name ="index"),
    path("ads", views.AdsView.as_view(), name ="ads"),
    path("banner/upload", views.UploadBanner, name ="upload_banner"),
    path("category", views.CategoryView.as_view(), name ="category"),
    path("category/create/", views.Category_Create, name ="category_create"),
    path("category/banner/view/<int:pk>", views.CategoryBanner, name ="modal_preview_category"),
    path("subcategory/create/", views.SubCategory_Create, name ="subcategory_create"),
]