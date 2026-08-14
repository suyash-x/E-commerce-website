from .models import tbl_cart
import json

def cart_context(request):
    email = request.session.get("email")
    if not email:
        return {
            'cart_count': 0,
            'cart_images_json': '[]'
        }
    
    cart_count = tbl_cart.objects.filter(userid=email).count()
    cart_images = []
    if cart_count > 0:
        # Get the 5 most recently added items
        cart_items_for_toast = list(tbl_cart.objects.filter(userid=email).order_by('-id').values('product_picture')[:5])
        cart_images = [item['product_picture'] for item in cart_items_for_toast]

    return {
        'cart_count': cart_count,
        'cart_images_json': json.dumps(cart_images)
    }