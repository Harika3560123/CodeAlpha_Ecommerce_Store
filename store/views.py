from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal
import json

from .models import Category, Product, Cart, CartItem, Order, OrderItem, UserProfile
from .forms import UserRegisterForm, UserLoginForm, CheckoutForm, UserProfileForm
from .context_processors import get_user_cart


def home(request):
    """Storefront homepage with hero banner, category showcases, and product grid."""
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:4]
    categories = Category.objects.all()

    # Search & Filter
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', '').strip()

    products = Product.objects.filter(is_active=True)

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(details__icontains=query)
        )

    # Sorting
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    # Pagination
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'products': page_obj,
        'selected_category': selected_category,
        'query': query,
        'sort': sort,
        'total_products': paginator.count,
    }
    return render(request, 'store/home.html', context)


def product_detail(request, slug):
    """Detailed view for a single product with specs, ratings, and related items."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    # Split details into bullet list if newline separated
    specs = [line.strip() for line in product.details.split('\n') if line.strip()] if product.details else []

    context = {
        'product': product,
        'related_products': related_products,
        'specs': specs,
    }
    return render(request, 'store/product_detail.html', context)


def cart_detail(request):
    """Shopping cart page with dynamic item updates, subtotal, and checkout link."""
    cart = get_user_cart(request)
    cart_items = cart.items.select_related('product').all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)


def cart_add(request, product_id):
    """Add a product to cart via standard POST or AJAX fetch."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_user_cart(request)

    # Determine quantity
    quantity = 1
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

    if quantity < 1:
        quantity = 1

    # Check stock
    if product.stock < 1:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'success': False, 'message': 'Product is currently out of stock.'}, status=400)
        messages.error(request, f"{product.name} is currently out of stock.")
        return redirect('product_detail', slug=product.slug)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            cart_item.quantity = product.stock
            cart_item.save()
            msg = f"Maximum available stock ({product.stock}) added for {product.name}."
        else:
            cart_item.quantity = new_quantity
            cart_item.save()
            msg = f"Updated {product.name} quantity to {cart_item.quantity} in your cart!"
    else:
        cart_item.quantity = min(quantity, product.stock)
        cart_item.save()
        msg = f"Added {product.name} to your cart!"

    # Response for AJAX
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.META.get('HTTP_ACCEPT', '')
    if is_ajax:
        return JsonResponse({
            'success': True,
            'message': msg,
            'cart_count': cart.total_items(),
            'cart_subtotal': str(cart.subtotal()),
        })

    messages.success(request, msg)
    # Redirect back to referring page or cart
    return redirect(request.META.get('HTTP_REFERER', 'cart_detail'))


def cart_update(request, item_id):
    """Update item quantity in cart with AJAX support."""
    cart = get_user_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        try:
            # Handle JSON body or Form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                quantity = int(data.get('quantity', 1))
            else:
                quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError, json.JSONDecodeError):
            quantity = 1

        if quantity <= 0:
            product_name = cart_item.product.name
            cart_item.delete()
            msg = f"Removed {product_name} from your cart."
        else:
            if quantity > cart_item.product.stock:
                cart_item.quantity = cart_item.product.stock
                cart_item.save()
                msg = f"Stock limit reached: set to {cart_item.product.stock} items."
            else:
                cart_item.quantity = quantity
                cart_item.save()
                msg = "Cart updated successfully."

        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json'
        if is_ajax:
            item_total = str(cart_item.item_total()) if cart_item.id else '0.00'
            return JsonResponse({
                'success': True,
                'message': msg,
                'cart_count': cart.total_items(),
                'item_total': item_total,
                'subtotal': str(cart.subtotal()),
                'tax': str(cart.tax()),
                'shipping': str(cart.shipping()),
                'grand_total': str(cart.grand_total()),
            })

        messages.success(request, msg)

    return redirect('cart_detail')


def cart_remove(request, item_id):
    """Remove product item from cart."""
    cart = get_user_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    name = cart_item.product.name
    cart_item.delete()

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        return JsonResponse({
            'success': True,
            'message': f"Removed {name} from cart.",
            'cart_count': cart.total_items(),
            'subtotal': str(cart.subtotal()),
            'tax': str(cart.tax()),
            'shipping': str(cart.shipping()),
            'grand_total': str(cart.grand_total()),
        })

    messages.info(request, f"Removed {name} from your cart.")
    return redirect('cart_detail')


def checkout(request):
    """Checkout page displaying address form and order summary."""
    cart = get_user_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.warning(request, "Your shopping cart is empty. Add products before checkout!")
        return redirect('home')

    # Initial data from user profile if logged in
    initial_data = {}
    if request.user.is_authenticated:
        initial_data.update({
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data.update({
                'phone': profile.phone,
                'address_line1': profile.address,
                'city': profile.city,
                'state': profile.state,
                'postal_code': profile.postal_code,
            })

    form = CheckoutForm(initial=initial_data)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'form': form,
    }
    return render(request, 'store/checkout.html', context)


def order_process(request):
    """Handle checkout submission, create Order and OrderItems, adjust stock, clear cart."""
    if request.method != 'POST':
        return redirect('checkout')

    cart = get_user_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('home')

    form = CheckoutForm(request.POST)
    if form.is_valid():
        order = form.save(commit=False)
        if request.user.is_authenticated:
            order.user = request.user

        # Price calculations
        order.subtotal = cart.subtotal()
        order.tax = cart.tax()
        order.shipping_cost = cart.shipping()
        order.total_amount = cart.grand_total()

        # Set payment status mock
        if order.payment_method in ['card', 'upi']:
            order.payment_status = 'Paid'
            order.status = 'Confirmed'
        else:
            order.payment_status = 'Pending'
            order.status = 'Processing'

        order.save()

        # Create Order Items and update product stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.get_effective_price(),
                quantity=item.quantity
            )
            # Deduct stock safely
            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
            else:
                item.product.stock = 0
            item.product.save()

        # Save address to user profile if user is authenticated
        if request.user.is_authenticated:
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.phone = order.phone
            profile.address = order.address_line1
            profile.city = order.city
            profile.state = order.state
            profile.postal_code = order.postal_code
            profile.save()

        # Clear cart items
        cart_items.delete()

        messages.success(request, f"Order #{order.order_number} has been placed successfully!")
        return redirect('order_success', order_number=order.order_number)
    else:
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'form': form,
        }
        messages.error(request, "Please correct the highlighted errors in the form.")
        return render(request, 'store/checkout.html', context)


def order_success(request, order_number):
    """Order confirmation and receipt page."""
    order = get_object_or_404(Order, order_number=order_number)
    items = order.items.select_related('product').all()

    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'store/order_success.html', context)


@login_required
def order_history(request):
    """View customer order history and order tracking."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')

    context = {
        'orders': orders,
    }
    return render(request, 'store/order_history.html', context)


def order_detail(request, order_number):
    """View receipt and status for a specific order."""
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    else:
        order = get_object_or_404(Order, order_number=order_number)

    items = order.items.select_related('product').all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'store/order_detail.html', context)


def user_register(request):
    """User registration view with auto-login upon successful signup."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user)

            # Auto login new user
            login(request, user)
            messages.success(request, f"Welcome to CodeAlpha Store, {user.first_name or user.username}! Your account has been created.")
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'store/register.html', {'form': form})


def user_login(request):
    """Custom styled login view with flash messages and demo credentials support."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'store/login.html', {'form': form})


def user_logout(request):
    """Logout view with redirect to home."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def user_profile(request):
    """User account settings and profile details."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if form.is_valid():
            form.save()
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'store/profile.html', context)


def about(request):
    """About page introducing the CodeAlpha E-commerce project."""
    return render(request, 'store/about.html')


def contact(request):
    """Contact page with interactive feedback toast."""
    if request.method == 'POST':
        name = request.POST.get('name', 'Visitor')
        messages.success(request, f"Thank you, {name}! Your message has been received. We will respond shortly.")
        return redirect('contact')
    return render(request, 'store/contact.html')
