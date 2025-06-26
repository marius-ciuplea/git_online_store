from django.db import models
from core.models import TimestampedModel


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    # Relație recursivă: o categorie poate avea un părinte.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = "Categories"
        # Adaugă o ordine implicită pentru categorii, de exemplu alfabetică.
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_ancestors(self):
        """
        Returnează o listă cu toate categoriile părinte, de la cea mai îndepărtată
        până la cea mai apropiată (pentru breadcrumbs, de exemplu).
        """
        ancestors = []
        current = self.parent
        while current:
            ancestors.insert(0, current)  # Inserează la început pentru a menține ordinea corectă.
            current = current.parent
        return ancestors

    def get_descendants(self):
        """
        Returnează o listă cu toate categoriile copil și sub-copil (descendenții),
        utilă pentru a naviga în jos în ierarhia de categorii.
        """
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            # Apelează recursiv metoda pentru fiecare copil, adunând toți descendenții.
            descendants.extend(child.get_descendants())
        return descendants

    def get_all_products(self):
        """
        Returnează toate produsele asociate acestei categorii și subcategoriilor sale,
        la orice nivel de adâncime.
        """
        # 1. Inițializează QuerySet-ul cu produsele direct legate de această categorie.
        # Folosim .order_by() fără argumente pentru a elimina orice ordonare implicită
        # înainte de a începe operațiile de unire.
        products_queryset = self.products.all().order_by()

        # 2. Parcurge toate categoriile copil directe.
        for child_category in self.children.all():
            # 3. Apelează recursiv metoda 'get_all_products' pentru fiecare subcategorie.
            
            child_products_queryset = child_category.get_all_products().order_by()
            
            # 4. Unește (UNION) QuerySet-ul curent de produse cu cel al subcategoriei.
            # Metoda .union() este mai robustă decât operatorul '|' pentru aceste scenarii.
            products_queryset = products_queryset.union(child_products_queryset)
            
        # 5. Returnează QuerySet-ul final, asigurându-te că toate produsele sunt unice.
        return products_queryset


class Product(TimestampedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['name'] # Ordonează produsele alfabetic după nume.

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returnează URL-ul canonic pentru instanța curentă a produsului.
        Util pentru a crea link-uri în template-uri sau în Django Admin.
        """
        from django.urls import reverse
        # Presupune un URL pattern numit 'product_detail' în namespace-ul 'products'.
        return reverse('products:product_detail', args=[self.slug])