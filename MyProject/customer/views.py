from django.shortcuts import render,redirect
from user.models import *
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    if not request.session.get("email"):
        messages.warning(request, 'Please login to access the dashboard.')
        return redirect('/user/login/')
    return render(request,'customer/index.html')
def profile(request):
    user_email=request.session.get("email")
    if not user_email:
        messages.warning(request, 'Please login to view your profile.')
        return redirect('/user/login/')

    try:
        user_profile = tbl_register.objects.get(email=user_email)
    except tbl_register.DoesNotExist:
        # This case is unlikely if session is managed well, but good for safety
        messages.error(request, 'User profile not found. Please login again.')
        if 'email' in request.session:
            del request.session['email']
        return redirect('/user/login/')

    if request.method=="POST":
        user_profile.name = request.POST.get("name", user_profile.name)
        user_profile.mobile = request.POST.get("mobile", user_profile.mobile)
        user_profile.address = request.POST.get("address", user_profile.address)

        if 'fu' in request.FILES:
            user_profile.profile_pic = request.FILES["fu"]

        user_profile.save()

        # Update session data to reflect changes immediately
        request.session['uname'] = user_profile.name
        request.session['upic'] = user_profile.profile_pic.url

        messages.success(request, 'User profile updated successfully.')
        return redirect('/customer/profile/')

    return render(request,'customer/profile.html',{"userinfo": user_profile})
def logout(request):
    user=request.session.get("email")
    data=""
    if user:
        del request.session["email"]
        del request.session["uname"]
        del request.session["upic"]
        del request.session["cartitem"]
        messages.success(request, 'You have been logged out successfully.')
        return redirect("/user/index/")
    return render(request,'customer/logout.html')

def products(request):
    return render(request,'customer/products.html')


def myorder(request):
    user=request.session.get("email")
    if not user:
        messages.warning(request, 'Please login to view your orders.')
        return redirect('/user/login/')
    data=tbl_order_info.objects.all().filter(userid=user)
    return render(request,'customer/myorder.html',{"data":data})
def orderdetail(request):
    if not request.session.get("email"):
        messages.warning(request, 'Please login to view order details.')
        return redirect('/user/login/')

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
