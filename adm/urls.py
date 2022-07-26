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
]