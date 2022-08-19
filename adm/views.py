#Django
from contextlib import redirect_stderr
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic import CreateView,UpdateView,DetailView,DeleteView, ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User

#Local
from .models import Banner,Category,SubCategory, Product, Cart, Order, Parcel, UserDetail
from .forms import AddNewBanner, AddCategory, AddSubCategory, AddProduct, CreateParcel, OrderStatus
from comics_pyc.functions import Show

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if(not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full.path(),
            self.get_login_url(),self.get_redirect_field_name())

        if not self.has_permission():
            return redirect('login')
        return super(UserAccessMixin, self).dispatch(request,*args,*kwargs)

class IndexView(UserAccessMixin,TemplateView):
    template_name = 'adm/index.html'
    permission_required = 'is_staff'

class ParcelView(UserAccessMixin,ListView):
    permission_required = 'is_staff'
    template_name = 'adm/parcel.html'
    model = Parcel

class NewParcelView(UserAccessMixin,CreateView):
    permission_required = 'is_staff'
    template_name = 'adm/new_parcel.html'
    model = Parcel
    form_class = CreateParcel
    success_url = reverse_lazy('adm:parcel')

class ParcelUpdateView(UserAccessMixin,UpdateView):
    permission_required = 'is_staff'
    template_name = 'adm/parcel_update.html'
    model = Parcel
    form_class = CreateParcel
    success_url = reverse_lazy('adm:parcel')

class ParcelDeleteView(UserAccessMixin,DeleteView):
    permission_required = 'is_staff'
    model = Parcel
    success_url = reverse_lazy('adm:parcel')

class AdsView(UserAccessMixin,TemplateView):
    template_name = 'adm/ads.html'
    permission_required = 'is_staff'
    form = AddNewBanner
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form']=self.form
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
        return context

class CategoryUpdateView(UserAccessMixin,UpdateView):
    model = Category
    template_name = "adm/category_update.html"
    form_class = AddCategory
    success_url = reverse_lazy('adm:category')
    permission_required = 'is_staff'

class CategoryDeleteView(UserAccessMixin,DeleteView):
    model = Category
    template_name = "adm/category_delete.html"
    success_url = reverse_lazy('adm:category')
    permission_required = 'is_staff'

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

    return render(request,template_name,{'banner_category':banner_category})

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

class SubCategoryDeleteView(UserAccessMixin,DeleteView):
    model = SubCategory
    template_name = "adm/category_delete.html"
    success_url = reverse_lazy('adm:category')
    permission_required = 'is_staff'

class ProductView(UserAccessMixin,ListView):
    model = Product
    template_name = "adm/product.html"
    paginate_by = 20
    permission_required = 'is_staff'

class CreateProductView(UserAccessMixin,CreateView):
    model = Product
    form_class = AddProduct
    template_name = "adm/product_create.html"
    success_url = reverse_lazy('adm:products')
    permission_required = 'is_staff'

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
            'form': form
        })

class OrdersView(UserAccessMixin,ListView):
    model = Order
    template_name = "adm/order.html"
    paginate_by = 20
    permission_required = 'is_staff'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['badge'] = 'success'
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
        return context

class OrderDeleteView(UserAccessMixin,DeleteView):
    permission_required = 'is_staff'
    model = Order
    template_name = "adm/order_delete.html"
    success_url = reverse_lazy('adm:orders')
 
class UsersView(UserAccessMixin,ListView):
    permission_required = 'is_staff'
    model = User
    template_name = 'adm/users.html'
    paginate_by = 20

class UsersDeleteView(UserAccessMixin,DeleteView):
    permission_required = 'is_staff'
    model = User
    template_name = "adm/users_delete.html"
    success_url = reverse_lazy('adm:users')

def UserDetailView(request,pk):
    permission_required = 'is_staff'
    model = UserDetail.objects.filter(user=pk)
    template_name = 'adm/users_detail.html'

    return render(request,template_name,{
        'object': model
    })

