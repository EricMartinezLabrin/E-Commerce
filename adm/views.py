#Django
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import CreateView,UpdateView,DetailView,DeleteView, ListView

#Local
from .models import Banner,Category,SubCategory, Product, Cart
from .forms import AddNewBanner, AddCategory, AddSubCategory, AddProduct

class IndexView(TemplateView):
    template_name = 'adm/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AdsView(TemplateView):
    template_name = 'adm/ads.html'
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

class CategoryView(TemplateView):
    template_name = 'adm/category.html'
    form_category = AddCategory
    form_subcategory = AddSubCategory

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

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = "adm/category_update.html"
    form_class = AddCategory
    success_url = reverse_lazy('adm:category')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "adm/category_delete.html"
    success_url = reverse_lazy('adm:category')

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

class SubCategoryUpdateView(UpdateView):
    model = SubCategory
    template_name = "adm/category_update.html"
    form_class = AddSubCategory
    success_url = reverse_lazy('adm:category')

class SubCategoryDeleteView(DeleteView):
    model = SubCategory
    template_name = "adm/category_delete.html"
    success_url = reverse_lazy('adm:category')

class ProductView(ListView):
    model = Product
    template_name = "adm/product.html"
    paginate_by = 20

class CreateProductView(CreateView):
    model = Product
    form_class = AddProduct
    template_name = "adm/product_create.html"
    success_url = reverse_lazy('adm:products')

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

class OrdersView(ListView):
    model = Cart
    template_name = "adm/order.html"
    paginate_by = 20

class OrdersDetailView(DetailView):
    model = Cart
    template_name = "adm/order_detail.html"

    def get_products(self):
        products = Cart.objects.filter(order=self.kwargs['pk'])
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = OrdersDetailView.get_products(self)
        return context