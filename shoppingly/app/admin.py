from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['id','title','selling_price','description','discounted_price','brand','category','product_image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
	list_display = ['user','customer','product','ordered_date','status','quantity']

