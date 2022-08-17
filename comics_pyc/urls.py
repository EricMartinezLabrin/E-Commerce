"""comics_pyc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required


#Local
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='home'),
    path('login', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('adm/', include('adm.urls')),
    path('all_products', views.AllProductsView.as_view(), name="all_products"),
    path('user/create', views.CreateUser, name="create_user"),
    path('categories/<int:pk>', views.CategoriesView.as_view(), name='categories'),
    path('details/<int:pk>', views.DetailView.as_view(), name='details'),
    path('cart', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>', views.addCart, name='add'),
    path('cart/remove/<int:product_id>', views.removeCart, name='remove'),
    path('cart/decrement/<int:product_id>', views.decrementCart, name='decrement'),
    path('checkout/', login_required(views.CheckoutView), name='checkout'),
    path('checkout/payment', login_required(views.paymentView), name='payment'),
    path('checkout/successfully', login_required(views.SuccessfullyView.as_view()), name="successfully"),
    path('checkout/failed', login_required(views.FailedView.as_view()), name="failed"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
