from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryDetailView

app_name = 'products'

urlpatterns = [
    # path('', views.product_list, name='product_list'),
    path('', ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    
]