from decimal import Decimal
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, client
from django.core.files.uploadedfile import SimpleUploadedFile
from eshop.models import Product, Category, Cart, CartProduct, Customer
from eshop.utils import recalc_cart
from eshop.views import AddToCartView, BaseView

User = get_user_model()


class ProductModelTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = User.objects.create(username='tester', password='password')
        cls.category = Category.objects.create(name='Notebooks', slug='notebooks')
        image = SimpleUploadedFile("notebook_image.jpg", content=b'', content_type="image/jpg")
        product = Product.objects.create(
            category=cls.category,
            title='something',
            slug='test-slug',
            image=image,
            description='about notebook',
            price=500,
        )
        cls.customer = Customer.objects.create(user=cls.user, phone="222222211", address="Address")
        cls.cart = Cart.objects.create(owner=cls.customer)
        cls.cart_product = CartProduct.objects.create(
            user=cls.customer,
            cart=cls.cart,
        )

    def test_add_to_cart(self):
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.final_price, Decimal(5000.00))

    def test_response_form_add_to_cart_view(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        response = AddToCartView.as_view()(request, ct_model="notebook", slug="test-slug")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart')
        client.get('/add-to-cart/notebook/test-slug/')
        self.assertEqual(response.status_code, 200)

    def test_mock_homepage(self):
        mock_data = mock.Mock(status_code=444)
        with mock.patch('eshop.views.BaseView.get', return_value=mock_data) as mock_data:
            factory = RequestFactory()
            request = factory.get('')
            request.user = self.user
            response = BaseView.as_view()(request)
            self.assertEqual(response.status_code, 444)


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get(':8000/')
        self.assertEqual(response.status_code, 200)

     def test_version(self):
         assert self.get('/').status_code == 200



    def test_title_max_length(self):
        product = Product.objects.get()
        max_length = product._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)
