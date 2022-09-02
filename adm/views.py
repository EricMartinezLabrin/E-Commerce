#Django
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic import CreateView,UpdateView,DetailView,DeleteView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

#Local
from .models import Banner,Category,SubCategory, Product, Cart, Order, Parcel, UserDetail, Region, Settings, Status
from .forms import AddNewBanner, AddCategory, AddSubCategory, AddProduct, CreateParcel, OrderStatus, SettingsForm, ProfileDetailForm, ProfileForm, CreateUser2
from comics_pyc.functions import Show
from comics_pyc.credentials import Credentials

#python
import requests
import mercadopago

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full.path(),
            self.get_login_url(),self.get_redirect_field_name())

        if not self.has_permission():
            return redirect('login')
        return super(UserAccessMixin, self).dispatch(request,*args,*kwargs)

class ProfileDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "is_staff"
    template_name = 'adm/profile.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class ProfileUpdateBasicView(PermissionRequiredMixin,UpdateView):
    model = User
    success_url = reverse_lazy('adm:profile')
    template_name = 'adm/settings_update.html'
    form_class = ProfileForm
    permission_required = 'is_staff'
    success_url = reverse_lazy('adm:profile_updated')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class ProfileUpdatedView(PermissionRequiredMixin, TemplateView):
    template_name = 'adm/profile_updated.html'
    permission_required = 'is_staff'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

def CheckProfile(request, pk):
    try:
        UserDetail.objects.get(pk=pk)
        return HttpResponseRedirect(reverse('adm:profile_update_others', args=(pk,)))
    except UserDetail.DoesNotExist:
        user = User.objects.get(pk=pk)
        try:
            region = Region.objects.get(pk=1)
        except Region.DoesNotExist:
            Region.objects.create(name="")
            region = Region.objects.get(pk=1)
        
        try:
            parcel = Parcel.objects.get(pk=1)
        except Parcel.DoesNotExist:
            Parcel.objects.create(name="")
            parcel = Parcel.objects.get(pk=1)
        UserDetail.objects.create(user=user, interior_number=0, region=region, parcel=parcel)
        return HttpResponseRedirect(reverse('adm:profile_update_others', args=(pk,)))

class ProfileUpdateOtherView(PermissionRequiredMixin,UpdateView):
    permission_required = 'is_staff'
    model = UserDetail
    form_class = ProfileDetailForm
    template_name = 'adm/settings_update.html'
    success_url = reverse_lazy('adm:profile_updated')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class PasswordChangeView(PermissionRequiredMixin, PasswordChangeView):
    template_name = 'adm/password_change_form.html'
    permission_required = "is_staff"
    success_url = reverse_lazy('adm:password_change_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class PasswordChangeDoneView(PasswordChangeDoneView):
    permission_required = "is_staff"
    template_name = 'adm/password_change_done.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class SettingsView(UserAccessMixin,TemplateView):
    permission_required = "is_staff"
    model = Settings
    template_name = 'adm/settings.html'
    
    try:
        settings = Settings.objects.get(pk=1)
    except:
        settings = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.settings
        context['data_settings'] = Show.settings_data()
        return context

class SettingsCreateView(UserAccessMixin,CreateView):
    permission_required = "is_staff"
    model = Settings
    form_class = SettingsForm
    template_name = 'adm/settings_create.html'
    success_url = reverse_lazy('adm:settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class SettingsUpdateView(UserAccessMixin,UpdateView):
    permission_required = "is_staff"
    model = Settings
    form_class = SettingsForm
    template_name = 'adm/settings_update.html'
    success_url = reverse_lazy('adm:settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class IndexView(UserAccessMixin,TemplateView):
    template_name = 'adm/index.html'
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class ParcelView(UserAccessMixin,ListView):
    permission_required = 'is_staff'
    template_name = 'adm/parcel.html'
    model = Parcel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class NewParcelView(UserAccessMixin,CreateView):
    permission_required = 'is_staff'
    template_name = 'adm/new_parcel.html'
    model = Parcel
    form_class = CreateParcel
    success_url = reverse_lazy('adm:parcel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class ParcelUpdateView(UserAccessMixin,UpdateView):
    permission_required = 'is_staff'
    template_name = 'adm/parcel_update.html'
    model = Parcel
    form_class = CreateParcel
    success_url = reverse_lazy('adm:parcel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class ParcelDeleteView(UserAccessMixin,DeleteView):
    permission_required = 'is_staff'
    model = Parcel
    success_url = reverse_lazy('adm:parcel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class AdsView(UserAccessMixin,ListView):
    template_name = 'adm/ads.html'
    permission_required = 'is_staff'
    model = Banner
    form = AddNewBanner
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=self.form
        context['data_settings'] = Show.settings_data()
        return context

class BannerUpdateView(UserAccessMixin,UpdateView):
    template_name = 'adm/ads_update.html'
    permission_required= 'is_staff'
    model = Banner
    form_class = AddNewBanner
    success_url = reverse_lazy('adm:ads')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class BannerDeleteView(UserAccessMixin, DeleteView):
    template_name = 'adm/banner_delete.html'
    model = Banner
    success_url = reverse_lazy('adm:ads')
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

def UploadBanner(request):
    if request.method == "POST":
        # Fetching the form data
        uploadedFile = request.FILES["uploadedFile"]
        name = request.POST["name"]

        # Saving the information in the database
        document = Banner(
            name = name,
            uploadedFile = uploadedFile
        )
        document.save()

    return HttpResponseRedirect(reverse_lazy("adm:ads"))

class CategoryView(UserAccessMixin,TemplateView):
    template_name = 'adm/category.html'
    form_category = AddCategory
    form_subcategory = AddSubCategory
    permission_required = 'is_staff'

    def find_categories(status=True, id=False):
        if id == False:
            categories = Category.objects.filter(status=status)
        else:
            categories = Category.objects.filter(status=status,id=id)[0]
        return categories

    def find_subcategories(status=True, id=False):
        if id == False:
            subcategories = SubCategory.objects.filter(status=status)
        else:
            subcategories = SubCategory.objects.filter(status=status,id=id)[0]
        return subcategories


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories']=CategoryView.find_categories()
        context['subcategories']=CategoryView.find_subcategories()
        context['form']=self.form_category
        context['form_subcategory']=self.form_subcategory
        context['data_settings'] = Show.settings_data()
        return context

class CategoryUpdateView(UserAccessMixin,UpdateView):
    model = Category
    template_name = "adm/category_update.html"
    form_class = AddCategory
    success_url = reverse_lazy('adm:category')
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class CategoryDeleteView(UserAccessMixin,DeleteView):
    model = Category
    template_name = "adm/category_delete.html"
    success_url = reverse_lazy('adm:category')
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

def Category_Create(request):
    if request.method == "POST":
        # Fetching the form data
        uploadedFile = request.FILES["banner"]
        name = request.POST["name"]

        # Saving the information in the database
        document = Category(
            name = name,
            banner = uploadedFile
        )
        document.save()

    return HttpResponseRedirect(reverse_lazy("adm:category"))

def CategoryBanner(request,pk):
    template_name = 'adm/modal_preview_category.html'
    banner_category = CategoryView.find_categories(id=pk)

    return render(request,template_name,{
        'banner_category':banner_category,
        'data_settings' : Show.settings_data
        })

def SubCategory_Create(request):
    if request.method == "POST":
        # Fetching the form data
        uploadedFile = request.FILES["banner"]
        name = request.POST["name"]
        subcategory = request.POST["subcategory"]
        subcategory = Category.objects.filter(pk=subcategory)[0]

        # Saving the information in the database
        document = SubCategory(
            name = name,
            banner = uploadedFile,
            subcategory = subcategory
        )
        document.save()

    return HttpResponseRedirect(reverse_lazy("adm:category"))

class SubCategoryUpdateView(UserAccessMixin,UpdateView):
    model = SubCategory
    template_name = "adm/category_update.html"
    form_class = AddSubCategory
    success_url = reverse_lazy('adm:category')
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class SubCategoryDeleteView(UserAccessMixin,DeleteView):
    model = SubCategory
    template_name = "adm/category_delete.html"
    success_url = reverse_lazy('adm:category')
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class ProductView(UserAccessMixin,ListView):
    model = Product
    template_name = "adm/product.html"
    paginate_by = 20
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class CreateProductView(UserAccessMixin,CreateView):
    model = Product
    form_class = AddProduct
    template_name = "adm/product_create.html"
    success_url = reverse_lazy('adm:products')
    permission_required = 'is_staff'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

def UpdateProduct(request,pk):
    product = Product.objects.get(pk=pk)
    form = AddProduct(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST":
        if form.is_valid():
            # Fetching the form data
            name = form.cleaned_data["name"]
            category = form.cleaned_data["category"]
            subcategory = form.cleaned_data["subcategory"]
            price = form.cleaned_data["price"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]

            # Saving the information in the database
            Product.objects.filter(pk=pk).update(
                name = name,
                category = category,
                subcategory = subcategory,
                price = price,
                description = description,
                image = image
            )
            
            return HttpResponseRedirect(reverse_lazy("adm:products"))
    else:
        return render(request,"adm/product_update.html",{
            'form': form,
            'data_settings' : Show.settings_data
        })

class OrdersView(UserAccessMixin,ListView):
    model = Order
    template_name = "adm/order.html"
    paginate_by = 20
    permission_required = 'is_staff'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['badge'] = 'success'
        context['data_settings'] = Show.settings_data()
        return context

class OrdersDetailView(UserAccessMixin,DetailView):
    model = Order
    template_name = "adm/order_detail.html"
    permission_required = 'is_staff'

    def get_products(self):
        products = Cart.objects.filter(order=self.kwargs['pk'])
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = OrdersDetailView.get_products(self)
        context['badge'] = Show.show_status_color(self.kwargs['pk'])
        context['data_settings'] = Show.settings_data()
        return context

class OrdersStatusUpdateView(UserAccessMixin,UpdateView):
    permission_required = 'is_staff'
    model = Order
    form_class = OrderStatus
    success_url = reverse_lazy('adm:orders')
    template_name = 'adm/order_status_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.kwargs['pk']
        context['data_settings'] = Show.settings_data()
        return context

class OrderDeleteView(UserAccessMixin,DeleteView):
    permission_required = 'is_staff'
    model = Order
    template_name = "adm/order_delete.html"
    success_url = reverse_lazy('adm:orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context
 
class UsersView(UserAccessMixin,ListView):
    permission_required = 'is_staff'
    model = User
    template_name = 'adm/users.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

class UsersDeleteView(UserAccessMixin,DeleteView):
    permission_required = 'is_staff'
    model = User
    template_name = "adm/users_delete.html"
    success_url = reverse_lazy('adm:users')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_settings'] = Show.settings_data()
        return context

def UserDetailView(request,pk):
    permission_required = 'is_staff'

    try:
        model = UserDetail.objects.get(user=pk)
    except:
        user = User.objects.get(pk=pk)
        region = Region.objects.get(pk=1)#Otros
        UserDetail.objects.create(user=user,interior_number=0,region=region)
        model = UserDetail.objects.get(user=pk)

    template_name = 'adm/users_detail.html'

    return render(request,template_name,{
        'object': model,
        'data_settings' : Show.settings_data
    })

def UsersCreateView(request):
    if request.method == 'POST':
        form = CreateUser2(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            is_staff = form.cleaned_data['is_staff']

            user = User.objects.create_user(username,email,password)
            user.is_staff = is_staff
            user.save()
            return HttpResponseRedirect(reverse_lazy('adm:users'))
    else:
        form = CreateUser2
        template_name = 'adm/users_create.html'
        return render(request,template_name,{
            'form':form,
            'data_settings' : Show.settings_data
        })

@csrf_exempt
def MercadoPagoView(request):
    # sdk = mercadopago.SDK(Credentials.mercadopago())
    # payment_data = {
    # "transaction_amount": float(request.POST.get("transaction_amount")),
    # "token": request.POST.get("token"),
    # "description": request.POST.get("description"),
    # "installments": int(request.POST.get("installments")),
    # "payment_method_id": request.POST.get("payment_method_id"),
    # "notification_url": Credentials.notification_url(),
    # "payer": {
    #     "email": request.POST.get("email"),
    #     "identification": {
    #         "number": request.POST.get("number")
    #     }
    # }
    # }

    # payment_response = sdk.payment().create(payment_data)
    # payment = payment_response["response"]

    # return render(request,'adm/mercadopago.html')
    id = request.POST['data']['id']
    token = Credentials.mercadopago()
    
    url = "https://api.mercadopago.com/v1/payments/"+id

    payload={}
    headers = {
    'Authorization': 'Bearer '+token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response = response.json()

    order_id = response['external_reference']
    status = response['status']

    if status == 'approved':
        status_id = 2
    elif status == 'pending':
        status_id = 1
    elif status == 'authorized':
        status_id = 1
    elif status == 'in_process':
        status_id = 7
    elif status == 'in_mediation':
        status_id = 8
    elif status == 'rejected':
        status_id = 5
    elif status == 'cancelled':
        status_id = 9
    elif status == 'refunded':
        status_id = 6
    elif status == 'charged_back':
        status_id = 10
    
    status_instance = Status.objects.get(pk=status_id)
    order = Order.objects.get(pk=order_id)
    order.status = status_instance
    order.save()

    print(response.text)
