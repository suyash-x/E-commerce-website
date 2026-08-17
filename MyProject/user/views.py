from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from random import *
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import F # Import F object for database operations
from django.urls import reverse # Add this import
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
        # Safely create the dictionary, skipping items where the product has been deleted.
        cart_quantities = {str(item.product.id): item.product_quantity for item in cart_items if item.product}

    md={
        "categories":cdata,
        "product":pdata,
        "cart_quantities": cart_quantities,
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
        # Safely calculate the price, defaulting None to 0
        price = product.product_price or 0
        discount = product.product_discount or 0
        discounted_price = price - (price * discount / 100)
        total_price = discounted_price * quantity

        # Using update_or_create to handle both adding and updating quantity
        cart_item, created = tbl_cart.objects.update_or_create(
            userid=user,
            product=product,
            defaults={
                'product_quantity': quantity,
                'total_price': total_price
            }
        )
    else:  # quantity is 0, so remove the item
        tbl_cart.objects.filter(userid=user, product=product).delete()
        toast_type = "cart_remove"

    # Prepare JSON response for the sticky toast and cart updates
    ccount = tbl_cart.objects.filter(userid=user).count()
    request.session["cartitem"] = ccount
    recent_items = tbl_cart.objects.filter(userid=user).order_by('-id')[:5]
    cart_images = []
    for item in recent_items:
        # Safely get URL, checking if product and picture exist
        if item.product and item.product.product_picture:
            cart_images.append(item.product.product_picture.url)
    
    response_data = {
        "type": toast_type,
        "item_name": product.product_name,
        "cart_count": ccount,
        "cart_images": cart_images,
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
        messages.success(request, 'Thank you for contacting us. We will get back to you shortly.') # Changed to success for consistency
        return redirect(reverse('user:contact'))
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
    return(render(request,"customer/profile.html")) # Corrected template path
    
def uprofile(request):
    return(render(request,"uprofile.html")) # Corrected template path
    
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
        return redirect(reverse('user:login'))
      else:
        tbl_register(name=Name,mobile=Mobile,email=Email,password=Password,address=Address,profile_pic=ppic).save()
        messages.success(request, 'You are registered successfully. Please login.')
        return redirect(reverse('user:login'))
    return render(request,'user/register.html')

def login(request):
    if request.method=="POST":
        Email=request.POST.get("email")
        Password=request.POST.get("password")
        x=tbl_register.objects.all().filter(email=Email,password=Password).first()
        if x:
            request.session["email"]=str(x.email)
            request.session["uname"]=str(x.name)
            # Safely get profile picture URL, provide a default if it doesn't exist
            if x.profile_pic:
                request.session["upic"] = x.profile_pic.url
            else:
                request.session["upic"] = "/static/images/default_avatar.png"
            ccount=tbl_cart.objects.filter(userid=Email).count()
            request.session["cartitem"]=ccount
            messages.success(request, 'Logged in successfully.')
            return redirect(reverse('customer:index'))
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
        # Safely create the dictionary, skipping items where the product has been deleted.
        cart_quantities = {str(item.product.id): item.product_quantity for item in cart_items if item.product}
    
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
    # Recalculate total to ensure data integrity and fix any stale prices
    for item in cartitem:
        if item.product:
            price = item.product.product_price if item.product.product_price is not None else 0
            discount = item.product.product_discount if item.product.product_discount is not None else 0
            discounted_price = price - (price * (discount / 100))
            
            # Self-heal: Update the item's total_price in the DB if it's incorrect
            correct_total = discounted_price * (item.product_quantity or 0)
            if item.total_price != correct_total:
                item.total_price = correct_total
                item.save()
            total += item.total_price
        else:
            # If product is deleted, ensure its contribution to total is zero
            item.delete() # Self-heal: remove cart items that point to nothing
    orderid="Suyash"+str(randint(1000,9999))
    if cartid is not None:
        item_to_remove = tbl_cart.objects.filter(id=cartid, userid=email).first()
        if item_to_remove:
            item_name = item_to_remove.product.product_name if item_to_remove.product else "Deleted Product"
            item_to_remove.delete()
            ccount = tbl_cart.objects.filter(userid=email).count()
            request.session["cartitem"] = ccount
            # This simple message is handled by the frontend JavaScript
            toast_data = {"type": "cart_remove", "item_name": item_name, "cart_count": ccount}
            messages.error(request, json.dumps(toast_data))
        return redirect(reverse('user:cart'))
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
                # Add safety check to ensure product exists before creating order item
                if x.product:
                    tbl_order_items.objects.create(
                        orderid=order,
                        product=x.product,
                        product_quantity=x.product_quantity,
                        total_price=x.total_price,
                    )
            cartitem.delete()
            ccount=tbl_cart.objects.filter(userid=email).count()
            request.session["cartitem"]=ccount
            messages.success(request, 'Order placed successfully.') # This message is handled by JS to show a modal and redirect
            return redirect(reverse('user:cart')) # Redirect to cart page after order

    return render(request,"user/cart.html",{"data":cartitem,"payable_amount":total})
