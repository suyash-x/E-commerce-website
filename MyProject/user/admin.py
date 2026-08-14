from django.contrib import admin
from .models import *

# Register your models here.
class tblcontactAdmin(admin.ModelAdmin):
    list_display=("id","name","mobile","email","message")
admin.site.register(tblcontact,tblcontactAdmin) 

class tblgalleryAdmin(admin.ModelAdmin):
    list_display=("id","title","picture")
admin.site.register(tblgallery,tblgalleryAdmin)  

 
class tblteamAdmin(admin.ModelAdmin):
    list_display=("id","name","designation","picture")
admin.site.register(tblteam,tblteamAdmin) 
  
class tbl_registerAdmin(admin.ModelAdmin):
    list_display=("name","mobile","email","password","address","profile_pic")
admin.site.register(tbl_register,tbl_registerAdmin)   

class tbl_categoryAdmin(admin.ModelAdmin):
    list_display=("id","category_name","category_picture")
admin.site.register(tbl_category,tbl_categoryAdmin)

class tbl_productAdmin(admin.ModelAdmin):
    list_display=("id","product_name","product_price","product_discount","product_description","product_weight","product_picture","category")
admin.site.register(tbl_product,tbl_productAdmin)

class tbl_cartAdmin(admin.ModelAdmin):
    list_display=("id","userid","pid","product_name","product_picture","product_price","discount_price","product_quantity","product_weight","total_price")
admin.site.register(tbl_cart,tbl_cartAdmin)

class tbl_orderAdmin(admin.ModelAdmin):
    list_display=("id","userid","pid","product_name","product_picture","product_price","discount_price","product_quantity","product_weight","total_price","status","order_date")
admin.site.register(tbl_order,tbl_orderAdmin)
class tbl_order_infoAdmin(admin.ModelAdmin):
    list_display=("userid","orderid","name","mobile","address","status","total_amount","order_date")
admin.site.register(tbl_order_info,tbl_order_infoAdmin) 
class tbl_order_itemsAdmin(admin.ModelAdmin):
    list_display=("orderid","product_name","product_picture","product_price","discount_price","product_quantity","product_weight","total_price")
admin.site.register(tbl_order_items,tbl_order_itemsAdmin)   