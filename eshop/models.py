from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

#1 Add Category
#2 Add Product
#3 Add CartProduct
#4 Cart
#5 Order

class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Category name")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(max_length=255, verbose_name="Product name")
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    description = models.TextField(verbose_name="description", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="price")

    def __str__(self):
        return self.title

class Notebook(Product):

    diagonal = models.CharField(max_length=255,verbose_name="Diagonal")
    display_type = models.CharField(max_length=255, verbose_name="Display type")
    procesor_freq = models.CharField(max_length=255, verbose_name="Processor freq.")
    ram = models.CharField(max_length=255, verbose_name="Ram")
    video = models.CharField(max_length=255, verbose_name="Video")
    time_without_charge = models.CharField(max_length=255, verbose_name="Time without charge")

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

class Smartphone(Product):

    diagonal = models.CharField(max_length=255, verbose_name="Diagonal")
    display_type = models.CharField(max_length=255, verbose_name="Display type")
    resolution = models.CharField(max_length=255, verbose_name="Resolution")
    accum_volume = models.CharField(max_length=255, verbose_name="Accum Volume")
    ram = models.CharField(max_length=255, verbose_name="Ram")
    sd = models.BooleanField(max_length=255, verbose_name="SD")
    sd_volume_max = models.CharField(max_length=255, verbose_name="SD volume max")
    main_cam_ap = models.CharField(max_length=255, verbose_name="Main cam")
    frontal_cam_ap = models.CharField(max_length=255, verbose_name="Frontal cam")

    def __str__(self):
        return "{} : {}".format(self.category_name, self.title)


class CartProduct(models.Model):

    user = models.ForeignKey("Customer",verbose_name='Buyers', on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Cart", on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type","object_id")
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Total amount")

    def __str__(self):
        return "Product {} (for cart)".format(self.product.title)

class Cart(models.Model):

    owner = models.ForeignKey("Customer", verbose_name="Owner", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9,decimal_places=2, verbose_name="Total amaut")

    def __str__(self):
        return str(self.id)

class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Telephone number")
    adress = models.CharField(max_length=255, verbose_name="Adress")

    def __str__(self):
        return "Buyer: {} {}".format(self.user.first_name, self.user.last_name)


