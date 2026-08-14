from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index),
    path('profile/', views.profile),
    path('logout/', views.logout),
    path('myorder/', views.myorder),
    path('orderdetail/', views.orderdetail),
]