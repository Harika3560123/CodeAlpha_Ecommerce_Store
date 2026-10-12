from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Category, Product, Cart, CartItem, Order, OrderItem, UserProfile


class StoreModelsAndViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create category
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Test category'
        )
        # Create product
        self.product = Product.objects.create(
            category=self.category,
            name='Test Wireless Headphones',
            slug='test-wireless-headphones',
            price=Decimal('100.00'),
            discount_price=Decimal('80.00'),
            stock=10,
            rating=Decimal('4.5'),
            reviews_count=5,
            is_active=True,
            is_featured=True
        )
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='Password123!'
        )

    def test_product_pricing_helpers(self):
        """Test effective price and discount calculation."""
        self.assertEqual(self.product.get_effective_price(), Decimal('80.00'))
        self.assertTrue(self.product.has_discount())
        self.assertEqual(self.product.discount_percent(), 20)
        self.assertTrue(self.product.in_stock())

    def test_homepage_view(self):
        """Test storefront home page loads properly."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NovaStore')
        self.assertContains(response, 'Test Wireless Headphones')

    def test_product_detail_view(self):
        """Test product details page loads with specs and price."""
        response = self.client.get(reverse('product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Wireless Headphones')
        self.assertContains(response, '$80.00')

    def test_cart_workflow(self):
        """Test adding item to cart, updating quantity, and removing."""
        # 1. Add to cart
        add_url = reverse('cart_add', kwargs={'product_id': self.product.id})
        response = self.client.post(add_url, {'quantity': 2}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_count'], 2)

        # 2. View cart page
        cart_url = reverse('cart_detail')
        response = self.client.get(cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Wireless Headphones')

        # 3. Update quantity
        cart = Cart.objects.first()
        item = cart.items.first()
        update_url = reverse('cart_update', kwargs={'item_id': item.id})
        response = self.client.post(
            update_url,
            data='{"quantity": 3}',
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)

        # 4. Remove item
        remove_url = reverse('cart_remove', kwargs={'item_id': item.id})
        response = self.client.get(remove_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.items.count(), 0)

    def test_checkout_and_order_processing(self):
        """Test complete order creation workflow."""
        # Add product to cart first
        self.client.post(reverse('cart_add', kwargs={'product_id': self.product.id}), {'quantity': 1})

        # Submit checkout form
        order_data = {
            'first_name': 'Harika',
            'last_name': 'Test',
            'email': 'harika@example.com',
            'phone': '+91 9999999999',
            'address_line1': '123 Test Street',
            'address_line2': '',
            'city': 'Hyderabad',
            'state': 'Telangana',
            'postal_code': '500001',
            'country': 'India',
            'payment_method': 'cod',
            'order_notes': 'Handle with care'
        }
        process_url = reverse('order_process')
        response = self.client.post(process_url, order_data)

        # Should redirect to order success page
        self.assertEqual(response.status_code, 302)
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.first_name, 'Harika')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)

        # Product stock should be decremented
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 9)

    def test_user_authentication_flow(self):
        """Test registration, login, profile, and logout."""
        # Registration
        reg_url = reverse('register')
        signup_data = {
            'username': 'newcustomer',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!'
        }
        response = self.client.post(reg_url, signup_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newcustomer').exists())

        # Logout
        self.client.get(reverse('logout'))

        # Login
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': 'newcustomer', 'password': 'SecurePassword123!'})
        self.assertEqual(response.status_code, 302)
