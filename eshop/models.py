from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

#1 Add Category
#2 Add Product
#3 Add CartProduct
#4 Cart
#5 Order
#6 Specifications

class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Category name")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    title = models.CharField(max_length=255, verbose_name="Product name")
    slug = models.SlugField(unique=True)
    image = models.ImageField()
    description = models.TextField(verbose_name="description", null=Ture)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="price")

    def __str__(self):
        return self.title

class CartProduct(models.Model):

    user = models.ForeignKey("Customer",verbose_name='Buyers', on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Cart", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Total amaut")

    def __str__(self):
        return "Product {} (for cart)".format(self.product.title)

class Cart(models.Model):

    owner = models.ForeignKey("Customer", verbose_name="Owner", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True)
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


class Specifications(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255, verbose_name="Name of Product for Specifications")

    def __str__(self):
        return "Specifications for product: {}".format(self.name)
