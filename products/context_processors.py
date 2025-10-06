from .models import ProductType, ProductLine, ProductConcern, Cart

def categories(request):
    """Makes product categories available to all templates."""
    return {
        'product_types': ProductType.objects.all(),
        'product_lines': ProductLine.objects.all(),
        'product_concerns': ProductConcern.objects.all(),
    }

def cart(request):
    """Makes cart item count available to all templates for the logged-in user."""
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            # Use filter().first() instead of get() to avoid crashing if cart doesn't exist
            cart_model = Cart.objects.filter(user=request.user).first()
            if cart_model:
                # This method now exists in the Cart model
                cart_item_count = cart_model.get_item_count()
        except Exception:
            # In case of any other unexpected errors, default to 0
            cart_item_count = 0
            
    return {'cart_item_count': cart_item_count}
