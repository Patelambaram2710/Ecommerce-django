from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Liked ,Order , Review
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProductForm
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from . mail_work import email,out_of_stock,complain_mail
import os

def place_order1(request,cart_id):
    if request.method == "POST" :
        address = request.POST['address']
        phone = address = request.POST['phone']
        customer = request.user
        cart_items = Cart.objects.filter(user=customer)
        number=len(cart_items)
        
        if not cart_items.exists():
            return HttpResponse('Cart is empty')

        orders = []

        for item in cart_items:
            if item.id==cart_id :
                order = Order(
                    product=item.product,
                    customer=customer,
                    cart_item_ids=str(item.id),
                    quantity=item.quantity,
                    price=item.product.price ,
                    address=address,
                    phone=phone,
                )
                order.save()
                orders.append(order)
                item.delete()
        
    return render(request,'place_order.html')