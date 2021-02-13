from django.test import TestCase
from decimal import Decimal
from unittest import mock

from django.test import TestCase, RequestFactory, client
from django.contrib.auth import get_user_model

from eshop.models import Category, Notebook, CartProduct, Cart, Customer
from eshop.views import recalc_cart, AddToCartView, BaseView

User = get_user_model()


class ShopTestCases(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='tester', password='password')
        self.category = Category.objects.create(name='Notebooks', slug='notebooks')
        self.notebook = Notebook.objects.create(
            category=self.category,
            title="Test Notebook",
            slug="test-slug",
            price=Decimal('5000.00'),
            diagonal="17,3",
            display_type="IPS",
            processor_freq="3.4 GHz",
            ram="6 GB",
            video="GeForce GTX",
            time_without_charge="10" "hours"
        )
        self.customer = Customer.objects.create(user=self.user, phone="222222211", address="Address")
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            content_objects=self.notebook
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

    # def test_version(client):
    #     assert client.get('/').status_code == 200
