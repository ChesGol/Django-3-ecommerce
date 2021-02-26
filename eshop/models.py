from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Category name'))
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name=_('Image'))
    description = models.TextField(verbose_name=_('Description'), null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('Price'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name=_('Customer'), on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name=_('Cart'), on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=_('Total price'))

    def __str__(self):
        return f"Product: {self.product.title} (for cart)"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name=_('Owner'), on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, verbose_name=_('Products'), related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0, verbose_name=_('Total products'))
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name=_('Total price'))
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name=_('User'), on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    address = models.CharField(max_length=255, verbose_name=_('Address'))
    orders = models.ManyToManyField('Order', blank=True, verbose_name=_('customer orders'), related_name='related_order')

    def __str__(self):
        return f"Buyer: {self.user.first_name} {self.user.last_name}"


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_PAID = 'paid'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_PAID, 'Order paid'),
        (STATUS_NEW, 'New order'),
        (STATUS_IN_PROGRESS, 'Order pending'),
        (STATUS_READY, 'Order ready'),
        (STATUS_COMPLETED, 'Order completed')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Self'),
        (BUYING_TYPE_DELIVERY, 'Delivery')
    )

    customer = models.ForeignKey(Customer, verbose_name=_('customer'), related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name=_('first_name'))
    last_name = models.CharField(max_length=255, verbose_name=_('last_name'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone'))
    cart = models.ForeignKey(Cart, verbose_name=_('Cart'), on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name=_('Address'))
    status = models.CharField(
        max_length=100,
        verbose_name=_('Order status'),
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name=_('buying_type'),
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name=_('Commentary'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Order created'))
    order_date = models.DateField(verbose_name=_('Order completed'), default=timezone.now)

    def __str__(self):
        return str(self.id)
