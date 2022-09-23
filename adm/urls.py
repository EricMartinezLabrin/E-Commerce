#django
from django.urls import path
from django.contrib.auth.decorators import login_required


from . import views

app_name = "adm"
urlpatterns = [
    #extension: /adm/
    path("", login_required(views.IndexView.as_view()), name ="index"),
    path("profile/<int:pk>", login_required(views.ProfileDetailView.as_view()), name ="profile"),
    path("profile/update/<int:pk>", login_required(views.ProfileUpdateBasicView.as_view()), name ="profile_update"),
    path("profile/checkdetails/<int:pk>", login_required(views.CheckProfile), name="check_details"),
    path("profile/update/detail/<int:pk>", login_required(views.ProfileUpdateOtherView.as_view()), name ="profile_update_others"),
    path('profile/password_change/',login_required(views.PasswordChangeView.as_view()), name='password_change'),
    path('profile/password-change/done/', login_required(views.PasswordChangeDoneView.as_view()), name='password_change_done'),
    path("profile/update/done", login_required(views.ProfileUpdatedView.as_view()), name ="profile_updated"),
    path("settings", login_required(views.SettingsView.as_view()), name ="settings"),
    path("settings/create", login_required(views.SettingsCreateView.as_view()), name ="settings_create"),
    path("settings/update/<int:pk>", login_required(views.SettingsUpdateView.as_view()), name ="settings_update"),
    path("ads", login_required(views.AdsView.as_view()), name ="ads"),
    path("ads/why", login_required(views.WhyView.as_view()), name ="why"),
    path("ads/why/update/<int:pk>", login_required(views.WhyUpdateView.as_view()), name ="why_update"),
    path("ads/why/delete/<int:pk>", login_required(views.WhyDeleteView.as_view()), name ="why_delete"),
    path("ads/banner/secondary/<int:pk>", login_required(views.SecondaryBannerView.as_view()), name ="secondary_banner"),
    path("ads/banner/update/<int:pk>", login_required(views.BannerUpdateView.as_view()), name ="banner_update"),
    path("ads/banner/delete/<int:pk>", login_required(views.BannerDeleteView.as_view()), name ="banner_delete"),
    path("parcel", login_required(views.ParcelView.as_view()), name ="parcel"),
    path("parcel/update/<int:pk>", login_required(views.ParcelUpdateView.as_view()), name ="parcel_update"),
    path("parcel/delete/<int:pk>", login_required(views.ParcelDeleteView.as_view()), name ="parcel_delete"),
    path("new_parcel", login_required(views.NewParcelView.as_view()), name ="new_parcel"),
    path("banner/upload", login_required(views.UploadBanner), name ="upload_banner"),
    path("category", login_required(views.CategoryView.as_view()), name ="category"),
    path("category/create/", login_required(views.Category_Create), name ="category_create"),
    path("category/delete/<int:pk>", login_required(views.CategoryDeleteView.as_view()), name ="category_delete"),
    path("category/banner/view/<int:pk>", login_required(views.CategoryBanner), name ="modal_preview_category"),
    path("category/update/<int:pk>", login_required(views.CategoryUpdateView.as_view()), name ="category_update"),
    path("subcategory/create/", login_required(views.SubCategory_Create), name ="subcategory_create"),
    path("subcategory/update/<int:pk>", login_required(views.SubCategoryUpdateView.as_view()), name ="subcategory_update"),
    path("subcategory/delete/<int:pk>", login_required(views.SubCategoryDeleteView.as_view()), name ="subcategory_delete"),
    path("products", login_required(views.ProductView.as_view()), name ="products"),
    path("products/create", login_required(views.CreateProductView.as_view()), name ="products_create"),
    path("products/update/<int:pk>", login_required(views.UpdateProduct), name ="products_update"),
    path("orders", login_required(views.OrdersView.as_view()), name ="orders"),
    path("orders/add/<int:order>", login_required(views.OrdersView.as_view()), name ="orders_add"),
    path("orders/detail/<int:pk>", login_required(views.OrdersDetailView.as_view()), name ="orders_detail"),
    path("orders/status/update/<int:pk>", login_required(views.OrdersStatusUpdateView.as_view()), name ="orders_status_update"),
    path("orders/delete/<int:pk>", login_required(views.OrderDeleteView.as_view()), name ="orders_delete"),
    path("users", login_required(views.UsersView.as_view()), name ="users"),
    path("users/new", login_required(views.UsersCreateView), name ="new_user"),
    path("users/delete/<int:pk>", login_required(views.UsersDeleteView.as_view()), name ="users_delete"),
    path("users/detail/<int:pk>", login_required(views.UserDetailView), name ="users_detail"),
    path("payment/mercadopago", views.MercadoPagoView, name ="mercadopago"),


]