import json
from django.urls import reverse
from .models import tbl_cart # Ensure tbl_cart is imported

def js_urls(request):
    urls = {
        'updateCartItemUrl': reverse('user:update_cart_item'),
        'userLoginUrl': reverse('user:login'),
        'userProductsUrl': reverse('user:products'),
        'customerIndexUrl': reverse('customer:index'),
        'userIndexUrl': reverse('user:index'),
        'userRegisterUrl': reverse('user:register'),
        'customerProfileUrl': reverse('customer:profile'),
        'customerLogoutUrl': reverse('customer:logout'),
        'customerMyOrderUrl': reverse('customer:myorder'),
        'customerOrderDetailUrl': reverse('customer:orderdetail'),
        'userCartUrl': reverse('user:cart'), # Ensure this is included
        'userProfileUrl': reverse('user:uprofile'), # Add this for the footer link
    }
    return {'js_urls': json.dumps(urls)}

def cart_context(request):
    cart_count = 0
    cart_images = []
    email = request.session.get("email")
    if email:
        cart_count = tbl_cart.objects.filter(userid=email).count()
        # Get the URLs of the most recent 5 items for the toast
        recent_items = tbl_cart.objects.filter(userid=email).select_related('product').order_by('-id')[:5]
        for item in recent_items:
            # Safely get URL, checking if product and picture exist
            if item.product and item.product.product_picture:
                cart_images.append(item.product.product_picture.url)

    return {
        'cart_count': cart_count,
        'cart_images_json': json.dumps(cart_images)
    }