from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('team/', views.team, name='team'),
    path('profile/', views.profile, name='profile'),
    path('uprofile/', views.uprofile, name='uprofile'),
    path('register/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    # This is the new URL for our AJAX functionality
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
]