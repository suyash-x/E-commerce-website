from django.urls import path
from . import views

app_name = 'customer'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('myorder/', views.myorder, name='myorder'),
    path('orderdetail/', views.orderdetail, name='orderdetail'),
]