import json
from django.urls import reverse

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