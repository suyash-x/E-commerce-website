from django.shortcuts import render, redirect
from user.models import *
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse # <--- ADD THIS IMPORT

# Create your views here.
def index(request):
    if not request.session.get("email"):
        messages.warning(request, 'Please login to access the dashboard.')
        return redirect(reverse('user:login')) # <--- USE reverse()
    return render(request,'customer/index.html')
def profile(request):
    user_email=request.session.get("email")
    if not user_email:
        messages.warning(request, 'Please login to view your profile.')
        return redirect(reverse('user:login')) # <--- USE reverse()

    try:
        user_profile = tbl_register.objects.get(email=user_email)
    except tbl_register.DoesNotExist:
        # This case is unlikely if session is managed well, but good for safety
        messages.error(request, 'User profile not found. Please login again.')
        if 'email' in request.session:
            request.session.flush() # Clear session on profile not found
        return redirect(reverse('user:login')) # <--- USE reverse()

    if request.method=="POST":
        user_profile.name = request.POST.get("name", user_profile.name)
        user_profile.mobile = request.POST.get("mobile", user_profile.mobile)
        user_profile.address = request.POST.get("address", user_profile.address)

        if 'fu' in request.FILES:
            user_profile.profile_pic = request.FILES["fu"]

        user_profile.save()

        # Update session data to reflect changes immediately
        request.session['uname'] = user_profile.name
        # Safely get profile picture URL, provide a default if it doesn't exist
        if user_profile.profile_pic:
            request.session['upic'] = user_profile.profile_pic.url
        else:
            request.session['upic'] = "/static/images/default_avatar.png"

        messages.success(request, 'Profile updated successfully.')
        return redirect(reverse('customer:profile')) # <--- USE reverse()

    return render(request,'customer/profile.html',{"userinfo": user_profile})
def logout(request):
    user=request.session.get("email")
    if user:
        request.session.flush() # Clears all session data at once
        messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('user:index')) # <--- USE reverse()

def products(request):
    return render(request,'customer/products.html')


def myorder(request):
    user=request.session.get("email")
    if not user:
        messages.warning(request, 'Please login to view your orders.')
        return redirect(reverse('user:login')) # <--- USE reverse()
    data=tbl_order_info.objects.all().filter(userid=user)
    return render(request,'customer/myorder.html',{"data":data})
def orderdetail(request):
    if not request.session.get("email"):
        messages.warning(request, 'Please login to view order details.')
        return redirect(reverse('user:login')) # <--- USE reverse()

    orderid=request.GET.get("oid")
    # Get the main order info object first
    order_info = tbl_order_info.objects.filter(orderid=orderid).first()
    
    # Then get the related items
    order_items = tbl_order_items.objects.filter(orderid=order_info) if order_info else []

    context = {
        "order": order_info,
        "items": order_items,
    }
    return render(request,'customer/orderdetail.html', context)
