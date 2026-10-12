from .models import Cart, Category


def get_user_cart(request):
    """Retrieve or create the cart for authenticated user or anonymous session."""
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        # Check if user has an existing cart
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            # Check if there is an anonymous session cart to merge
            session_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
            if session_cart:
                session_cart.user = request.user
                session_cart.save()
                cart = session_cart
            else:
                cart = Cart.objects.create(user=request.user)
        else:
            # If there is also an anonymous session cart, merge its items into user's cart
            session_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
            if session_cart and session_cart != cart:
                for item in session_cart.items.all():
                    existing_item = cart.items.filter(product=item.product).first()
                    if existing_item:
                        existing_item.quantity += item.quantity
                        existing_item.save()
                    else:
                        item.cart = cart
                        item.save()
                session_cart.delete()
    else:
        cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()
        if not cart:
            cart = Cart.objects.create(session_key=session_key)

    return cart


def cart_context(request):
    """Context processor providing cart information and category navigation to all templates."""
    try:
        cart = get_user_cart(request)
        cart_count = cart.total_items()
    except Exception:
        cart = None
        cart_count = 0

    categories = Category.objects.all()

    return {
        'cart': cart,
        'cart_count': cart_count,
        'nav_categories': categories,
    }
