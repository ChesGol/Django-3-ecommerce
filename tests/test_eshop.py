from decimal import Decimal
from unittest import mock
import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from eshop.models import Product, Category, Cart, CartProduct, Customer
from eshop.utils import recalc_cart
from eshop.views import AddToCartView, BaseView

User = get_user_model()


@pytest.mark.django_db
def test_index(client: Client):
    assert client.get('').status_code == 200


class ProductModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='tester', password='password')
        self.category = Category.objects.create(name='Notebooks', slug='notebooks')
        self.image = SimpleUploadedFile("notebook_image.jpg", content=b'', content_type="image/jpg")
        self.product = Product.objects.create(
            category=self.category,
            title='something',
            slug='test-slug',
            image=self.image,
            description='about notebook',
            price=500,
        )
        self.customer = Customer.objects.create(user=self.user, phone="222222211", address="Address")
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            product=self.product
        )

    def test_add_to_cart(self):
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.final_price, Decimal(500.00))

    # def test_response_form_add_to_cart_view(self):
    #     factory = RequestFactory()
    #     request = factory.get('')
    #     request.user = self.user
    #     response = AddToCartView.as_view()(request, category='notebooks', slug='test-slug')
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, '/cart')
    #     client.get('/add-to-cart/notebooks/test-slug/')
    #     self.assertEqual(response.status_code, 200)

    def test_mock_homepage(self):
        mock_data = mock.Mock(status_code=444)
        with mock.patch('eshop.views.BaseView.get', return_value=mock_data):
            factory = RequestFactory()
            request = factory.get('')
            request.user = self.user
            response = BaseView.as_view()(request)
            self.assertEqual(response.status_code, 444)

# @mark.django_db
# def test_title_max_length():
#     product = Product.objects.get()
#     max_length = product._meta.get_field('title').max_length
#     self.assertEqual(max_length, 255)
