from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from random import *
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
# Create your views here.

def index(request):
    cdata=tbl_category.objects.all().order_by("-id")[0:6]
    pdata=tbl_product.objects.all().order_by("-product_discount")[0:8]
    
    cart_quantities = {}
    email = request.session.get("email")
    if email:
        cart_items = tbl_cart.objects.filter(userid=email)
        cart_quantities = {str(item.pid): item.product_quantity for item in cart_items}

    md={
        "categories":cdata,
        "product":pdata,
        "cart_quantities": cart_quantities
    }
    return render(request,"user/index.html",md)

@require_POST
def update_cart_item(request):
    user = request.session.get("email")
    if not user:
        return JsonResponse({'status': 'error', 'message': 'Please login first to perform this action.'}, status=401)

    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        quantity = int(data.get('quantity'))
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    try:
        product = tbl_product.objects.get(id=product_id)
    except tbl_product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    toast_type = "cart_add"
    if quantity > 0:
        # Using update_or_create to handle both adding and updating quantity
        tbl_cart.objects.update_or_create(
            userid=user,
            pid=product.id,
            defaults={
                'product_name': product.product_name,
                'product_picture': product.product_picture,
                'product_price': product.product_price,
                'discount_price': product.product_discount,
                'product_weight': product.product_weight,
                'product_quantity': quantity,
                'total_price': product.product_price * quantity
            }
        )
    else:  # quantity is 0, so remove the item
        tbl_cart.objects.filter(userid=user, pid=product.id).delete()
        toast_type = "cart_remove"

    # Prepare JSON response for the sticky toast and cart updates
    ccount = tbl_cart.objects.filter(userid=user).count()
    request.session["cartitem"] = ccount
    cart_items_for_toast = list(tbl_cart.objects.filter(userid=user).order_by('-id').values('product_picture')[:5])
    
    response_data = {
        "type": toast_type,
        "item_name": product.product_name,
        "cart_count": ccount,
        "cart_images": [item['product_picture'] for item in cart_items_for_toast],
        "status": "success"
    }
    
    return JsonResponse(response_data)

def contact(request):
    if request.method=="POST":
        a=request.POST.get("name")
        b=request.POST.get("mobile")
        c=request.POST.get("email")
        d=request.POST.get("message")
        tblcontact(name=a,mobile=b,email=c,message=d).save()
        messages.info(request, 'Thank you for contacting us. We will get back to you shortly.')
        return redirect('/user/contact/')
    mydict={}
    return render(request,"user/contact.html",mydict)

def about(request):
    return render(request,"user/about.html")

def gallery(request):
    data=tblgallery.objects.all()
    mydict={"gallerydata":data}
    return render(request,"user/gallery.html",mydict)

def team(request):
    data=tblteam.objects.all()
    mydict={"teamdata":data}
    return render(request,"user/team.html",mydict)
def profile(request):
    return(render(request,"user/profile.html"))
    
def uprofile(request):
    return(render(request,"uprofile.html"))
    
def registration(request):
    if request.method=="POST":
      Name=request.POST.get("name")
      Email=request.POST.get("email")
      Mobile=request.POST.get("mobile")
      Password=request.POST.get("password")
      Address=request.POST.get("address")
      ppic=request.FILES["fu"]
      # Use .exists() for a more efficient database query
      if tbl_register.objects.filter(email=Email).exists():
        messages.warning(request, 'You are already registered. Please login.')
        return redirect('/user/login/')
      else:
        tbl_register(name=Name,mobile=Mobile,email=Email,password=Password,address=Address,profile_pic=ppic).save()
        messages.success(request, 'You are registered successfully. Please login.')
        return redirect('/user/login/')
    return render(request,'user/register.html')

def login(request):
    if request.method=="POST":
        Email=request.POST.get("email")
        Password=request.POST.get("password")
        x=tbl_register.objects.all().filter(email=Email,password=Password).first()
        if x:
            request.session["email"]=str(x.email)
            request.session["uname"]=str(x.name)
            request.session["upic"]=str(x.profile_pic)
            ccount=tbl_cart.objects.filter(userid=Email).count()
            request.session["cartitem"]=ccount
            messages.success(request, 'Logged in successfully.')
            return redirect('/customer/index/')
        else:
            return render(request,"user/login.html",{"msg":"Invalid id or pass"})
    
    return render(request,'user/login.html')

def dashboard(request):
    return(render(request,"user/dashboard.html"))

def products(request):
    x=request.GET.get("cid")
    cdata=tbl_category.objects.all().order_by("-id")
    pdata=""
    if x is not None:
        pdata=tbl_product.objects.all().filter(category=x)
    else:
        pdata=tbl_product.objects.all().order_by("-id")
    
    cart_quantities = {}
    email = request.session.get("email")
    if email:
        cart_items = tbl_cart.objects.filter(userid=email)
        cart_quantities = {str(item.pid): item.product_quantity for item in cart_items}
    
    md={
        "categories":cdata,
        "product":pdata,
        "cart_quantities": cart_quantities
    }
    return render(request,"user/products.html",md)

def cart(request):
    cartid=request.GET.get("cid")
    email=request.session.get("email")
    cartitem=tbl_cart.objects.all().filter(userid=email)
    total=0
    for cart in cartitem:
        total+=cart.total_price
    orderid="Suyash"+str(randint(1000,9999))
    if cartid is not None:
        item_to_remove = tbl_cart.objects.filter(id=cartid, userid=email).first()
        if item_to_remove:
            item_name = item_to_remove.product_name
            item_to_remove.delete()
            ccount = tbl_cart.objects.filter(userid=email).count()
            request.session["cartitem"] = ccount
            cart_items_for_toast = list(tbl_cart.objects.filter(userid=email).order_by('-id').values('product_picture')[:5])
            toast_data = {
                "type": "cart_remove",
                "item_name": item_name,
                "cart_count": ccount,
                "cart_images": [item['product_picture'] for item in cart_items_for_toast]
            }
            messages.error(request, json.dumps(toast_data))
        return redirect('/user/cart/')
    if email:
        if request.method=="POST":
            name=request.POST.get("name")
            mobile=request.POST.get("mobile")
            address=request.POST.get("address")
            order=tbl_order_info.objects.create(
                userid=email,
                orderid=orderid,
                name=name,
                mobile=mobile,
                address=address,
                total_amount=total,
            )
            # The 'order' variable now holds the tbl_order_info instance.
            for x in cartitem:
                # FIX 1: Corrected model name from tbl_order_item to tbl_order_items
                # FIX 2: Passed the 'order' instance to the ForeignKey field.
                tbl_order_items.objects.create(
                    orderid=order,
                    product_name=x.product_name,
                    product_picture=x.product_picture,
                    product_quantity=x.product_quantity,
                    product_weight=x.product_weight,
                    total_price=x.total_price,
                )
            cartitem.delete()
            ccount=tbl_cart.objects.filter(userid=email).count()
            request.session["cartitem"]=ccount
            messages.success(request, 'Order placed successfully.')
            return redirect('/user/cart/')

    return render(request,"user/cart.html",{"data":cartitem,"payable_amount":total})
