from django.shortcuts import render, redirect
from .models import Customer, Cart, Product, OrderPlaced
from django.views import View
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




class home(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        tv = Product.objects.filter(category='T')

        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'tv':tv})




#@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProductDetail(View):
    def get(self,request,id):
        prod = Product.objects.get(id = id)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product = prod.id) & Q(user = request.user)).exists()
        return render(request,'app/productdetail.html',{'prod':prod,'item_already_in_cart':item_already_in_cart})


@login_required(login_url='/login/')
def add_to_cart(request):
    user = request.user 
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product = product).save()
    return redirect('/cart/')

@login_required(login_url='/login/')
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product =[p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity *p.product.discounted_price)
                amount += tempamount
                total_amount = amount+shipping_amount
            return render(request,'app/addtocart.html',{'cart':cart,'amount':amount,'total_amount':total_amount})
        else:
            return render(request,'app/emptycart.html')

@login_required(login_url='/login/')
def plus_cart(request):
    if request.method =='GET':
        user = request.user
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity +=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product =[p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity *p.product.discounted_price)
            amount += tempamount
            total_amount = amount+shipping_amount

        data = {
        'quantity': c.quantity,
        'amount': amount,
        'total_amount': total_amount 
            }  
    return JsonResponse(data)     

@login_required(login_url='/login/')
def minus_cart(request):
    if request.method =='GET':
        user = request.user
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product =[p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity *p.product.discounted_price)
            amount += tempamount


        data = {
        'quantity': c.quantity,
        'amount': amount,
        'total_amount': amount + shipping_amount
            }  
    return JsonResponse(data)

@login_required(login_url='/login/')
def remove_cart(request):
    if request.method =='GET':
        user = request.user
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id)& Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product =[p for p in Cart.objects.all() if p.user == user]
        for p in cart_product:
            tempamount = (p.quantity *p.product.discounted_price)
            amount += tempamount

        data = {
        'quantity': c.quantity,
        'amount': amount,
        'total_amount': amount + shipping_amount 
            }  
    return JsonResponse(data) 


def buy_now(request):
 return render(request, 'app/buynow.html')

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            locality = form.cleaned_data['locality']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            cusobj = Customer(user=usr, name=name,city=city, state=state, locality=locality, zipcode=zipcode)
            cusobj.save()
            messages.success(request,'Congratulations !! Profile Updated Successfully')

        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

@login_required(login_url='/login/')
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add ,'active':'btn-primary'})

@login_required(login_url='/login/')
def orders(request):
    user = request.user
    order = OrderPlaced.objects.filter(user=user)
    return render(request, 'app/orders.html',{'order':order})

@login_required(login_url='/login/')
def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class customerregistration(View):
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations, Registration Successful !!')
            form.save()
        return redirect('/login/')
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})

@login_required(login_url='/login/')
def checkout(request):
    user =request.user 
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product =[p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity *p.product.discounted_price)
            print(tempamount)
            amount += tempamount

        total_amount = amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add, 'cart':cart_items, 'total_amount':total_amount})

@login_required(login_url='/login/')
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    if custid:
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product= c.product, quantity =c.quantity).save()
            c.delete()
        return redirect("/orders/")
    else:
        messages.info(request,'No Address Found, Please create Address to coninue !!')
        return redirect('/profile/')
