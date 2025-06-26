# products/admin.py
from django.contrib import admin
from .models import Category, Product

# --- Inline pentru Subcategorii (Copii) ---
class CategoryInline(admin.TabularInline): # Sau admin.StackedInline pentru un aspect diferit
    model = Category
    fk_name = 'parent' # Specifică câmpul ForeignKey care leagă copilul de părinte
    extra = 1 # Câte formulare goale să afișeze pentru a adăuga subcategorii noi
    fields = ['name', 'slug'] # Câmpurile pe care vrei să le editezi direct în inline
    prepopulated_fields = {'slug': ('name',)} # Pre-populează slug-ul pentru subcategorii


# --- Inline pentru Produse ---
class ProductInline(admin.TabularInline): # Sau admin.StackedInline
    model = Product
    extra = 1 # Câte formulare goale să afișeze pentru a adăuga produse noi
    fields = ['name', 'slug', 'price', 'stock', 'available'] # Câmpurile relevante ale produsului
    prepopulated_fields = {'slug': ('name',)}
    
    # Dacă vrei să poți edita aceste câmpuri direct în inline
    # list_editable = ['price', 'stock', 'available'] # Nu se poate folosi list_editable direct în inlines

    # Poți adăuga un link către pagina de editare a produsului
    show_change_link = True 


# --- Înregistrarea CategoryAdmin (modificată) ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['parent']
    search_fields = ['name']
    ordering = ['name']

    # Adaugă inlines-urile aici!
    inlines = [CategoryInline, ProductInline] # <-- Aici le adaugi


# --- Înregistrarea ProductAdmin (nemodificată sau cu modificări minore) ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'category', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    raw_id_fields = ['category']
    date_hierarchy = 'created_at'