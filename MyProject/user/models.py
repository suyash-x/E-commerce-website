from django.db import models

# Create your models here.
# tblcontact

class tblcontact(models.Model):
    name=models.CharField(max_length=50,null=True)
    mobile=models.CharField(max_length=15,null=True)
    email=models.CharField(max_length=50,null=True)
    message=models.TextField(null=True)
    
class tbl_register(models.Model):
    name=models.CharField(max_length=50,null=True)
    mobile=models.CharField(max_length=15,null=True)
    email=models.EmailField(primary_key=True)
    # CRITICAL SECURITY RISK: Storing plain-text passwords.
    # This should be migrated to use Django's built-in User model for secure password hashing.
    password=models.CharField(max_length=128,null=True)
    address=models.TextField(null=True)
    profile_pic=models.ImageField(upload_to="profile/",null=True)




class tblgallery(models.Model):
    title=models.CharField(max_length=200,null=True)
    picture=models.ImageField(upload_to="gallery/",null=True)   

class tblteam(models.Model):
    name=models.CharField(max_length=200,null=True)
    designation=models.CharField(max_length=200,null=True)
    picture=models.ImageField(upload_to="team/",null=True)  
    
class tbl_category(models.Model):
    category_name=models.CharField(max_length=80,null=True)
    category_picture=models.ImageField(upload_to="category/",null=True)
    def __str__(self):
        return self.category_name


class tbl_product(models.Model):
    product_name=models.CharField(max_length=80,null=True)
    product_price=models.FloatField(null=True)
    product_discount=models.FloatField(null=True)
    product_description=models.TextField(null=True)
    product_weight=models.CharField(null=True)
    product_picture=models.ImageField(upload_to="product/",null=True)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE,null=True)
    
class tbl_cart(models.Model):
    userid=models.CharField(max_length=50,null=True)
    # Use a ForeignKey to link directly to the product. This is the correct approach.
    product=models.ForeignKey(tbl_product, on_delete=models.CASCADE, null=True)
    product_quantity=models.IntegerField(null=True)
    total_price=models.FloatField(null=True)

class tbl_order_info(models.Model):
    userid=models.CharField(max_length=50,null=True)
    orderid=models.CharField(max_length=100,null=True)
    name=models.CharField(max_length=50,null=True)
    mobile=models.CharField(max_length=15,null=True)
    address=models.TextField(null=True)
    status=models.CharField(max_length=100,default="pending")
    total_amount=models.CharField(max_length=100,null=True)
    order_date=models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.orderid
    

class tbl_order_items(models.Model):
    orderid= models.ForeignKey('tbl_order_info', on_delete=models.CASCADE)
    # Use a ForeignKey. SET_NULL is safer for order history.
    # If a product is deleted, the order item remains but points to null.
    product=models.ForeignKey(tbl_product, on_delete=models.SET_NULL, null=True)
    product_quantity=models.IntegerField(null=True)
    total_price=models.FloatField(null=True)