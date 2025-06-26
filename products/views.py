from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    
class ProductDetailView(DetailView): # <--- New DetailView CBV
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product' # Will be available as 'product' in the template

    # You might want to filter for available products here too
    def get_queryset(self):
        return super().get_queryset().filter(available=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        current_product = self.object
        
        product_category = current_product.category
        
        ancestors = product_category.get_ancestors()
        
        context['product_category'] = product_category
        context['ancestors'] = ancestors
        
        return context
    
class CategoryDetailView(DetailView): # O nouă Class-Based View pentru detalii categorie
    model = Category
    template_name = 'products/category_detail.html' # Un template dedicat
    context_object_name = 'category' # Obiectul curent va fi 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_category = self.object # Categoria curentă

        # Obține strămoșii pentru breadcrumb
        context['ancestors'] = current_category.get_ancestors()
        
        # Opțional: Poți pasa și produsele direct legate de această categorie
        context['products_in_category'] = current_category.products.all().filter(available=True)
        
        # Opțional: Poți pasa și subcategoriile direct legate
        context['child_categories'] = current_category.children.all()

        return context