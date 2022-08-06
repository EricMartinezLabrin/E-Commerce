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
    path("category/delete/<int:pk>", views.CategoryDeleteView.as_view(), name ="category_delete"),
    path("category/banner/view/<int:pk>", views.CategoryBanner, name ="modal_preview_category"),
    path("category/update/<int:pk>", views.CategoryUpdateView.as_view(), name ="category_update"),
    path("subcategory/create/", views.SubCategory_Create, name ="subcategory_create"),
    path("subcategory/update/<int:pk>", views.SubCategoryUpdateView.as_view(), name ="subcategory_update"),
    path("subcategory/delete/<int:pk>", views.SubCategoryDeleteView.as_view(), name ="subcategory_delete"),
    path("products", views.ProductView.as_view(), name ="products"),
    path("products/create", views.CreateProductView.as_view(), name ="products_create"),
    path("products/update/<int:pk>", views.UpdateProduct, name ="products_update"),
    path("orders", views.OrdersView.as_view(), name ="orders"),
    path("orders/detail/<int:pk>", views.OrdersDetailView.as_view(), name ="orders_detail"),

]