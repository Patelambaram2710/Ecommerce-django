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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect to a page after login
    else:
        form = AuthenticationForm()
    return render(request, 'loginaccount.html', {'form': form})

from django.http import HttpResponse

def index(request):
    products = Product.objects.all()
    out_of_stock(request)
  
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()
    return render(request, "index.html", {'products': products, 'cart_item_count': cart_item_count})
from django.shortcuts import render
from .models import Product

def mobile(request):
    products = Product.objects.filter(category__name='mobile')

    # Get price range from request
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on price
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'category.html', {
        'products': products,
    })
def tv(request):
    products = Product.objects.filter(category__name='tv')

    # Get price range from request
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on price
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'category.html', {
        'products': products,
    })
def speaker(request):
    products = Product.objects.filter(category__name='speaker')

    # Get price range from request
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on price
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'category.html', {
        'products': products,
    })

def watch(request):
    products = Product.objects.filter(category__name='watch')

    # Get price range from request
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on price
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'category.html', {
        'products': products,
    })

def ac(request):
    products = Product.objects.filter(category__name='Air_conditionar')

    # Get price range from request
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on price
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'category.html', {
        'products': products,
    })

def laptop(request):
    products = Product.objects.filter(category__name='laptop')

    # Get price range from request
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter products based on price
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'category.html', {
        'products': products,
    })


@login_required(login_url='login')
def about(request):
    success = False
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success = True
            return render(request, 'about.html', {'form': form, 'success': success,'company' : 'SOFTV','year':2004})
    else:
        form = ProductForm()
    return render(request, 'about.html', {'form': form, 'success': success,'company' :'SOFTV','year':2004})

@login_required(login_url='login') 

def add_to_cart(request, product_id):
    # Get the product from the database
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(
        product=product, 
        user=request.user,  # Assuming the cart is associated with the logged-in user
    )

  
    if product.quantity >= cart_item.quantity + 1:
        # Always increase the quantity, whether it's newly created or already exists
        cart_item.quantity += 1  
        cart_item.save()  

        
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return HttpResponseRedirect(referer)
        else:
            return redirect('index')
    else:
        # If the requested quantity exceeds available product stock
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return HttpResponseRedirect(referer)


    
   

def increase(request,id) :
    car = get_object_or_404(Cart, id=id)
    prod = get_object_or_404(Product,id=car.product.id)

    if(prod.quantity >= car.quantity) :
        car.quantity += 1
        prod.quantity-=1
        car.save()
        prod.save()
        return redirect('cart')
    else :
        return redirect('cart')

def decrease(request,id) :
    
    car = get_object_or_404(Cart, id=id)
    prod = get_object_or_404(Product, id=car.product.id)

    if(prod.quantity > car.quantity) :
        car.quantity -=1
        prod.quantity+=1
        car.save()
        prod.save()
    return redirect('cart')

@login_required(login_url='login') 
def cart_view(request):
    
    cart_items = Cart.objects.filter(user=request.user)
    # for i in pr :
        # if (i.name == cart_items.product.name) :
            # qua=i.quantity
    return render(request, 'cart.html', {'cart_items': cart_items })

@login_required(login_url='login')  
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login') 
def remove_from_order(request, item_id):
    order_item = get_object_or_404(Order, id=item_id, customer=request.user)
    order_item.delete()
    return redirect('orders')

@login_required(login_url='login')  
def add_to_liked(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    liked_item, created = Liked.objects.get_or_create(user=request.user, product=product)
    if not created:
        liked_item.quantity += 1
        liked_item.save()
    return redirect('index')

@login_required(login_url='login')  
def liked_view(request):
    liked_items = Liked.objects.filter(user=request.user)
    return render(request, 'liked.html', {'liked_items': liked_items})

@login_required(login_url='login') 
def remove_from_liked(request, item_id):
    liked_item = get_object_or_404(Liked, id=item_id, user=request.user)
    liked_item.delete()
    return redirect('liked')

def category(request, category_id):
    # Get the category by ID
    selected_category = get_object_or_404(Category, id=category_id)
    
    # Get all products in the selected category
    products = Product.objects.filter(category=selected_category)
    
    context = {
        'selected_category': selected_category,
        'products': products,
    }
    return render(request, 'category.html', context)


def some_view(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
       
    }
    return render(request, 'some_template.html', context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product)

    return render(request, 'product_detail.html', {'product': product,'reviews':reviews})

def tv_products(request):
    products = Product.objects.filter(category__name='tv')
    return render(request, 'tv.html', {'products': products})

def phone_products(request):
    products = Product.objects.filter(category__name='mobile')
    return render(request, 'phone.html', {'products': products})

def speaker_products(request):
    products = Product.objects.filter(category__name='speaker')
    return render(request, 'speaker.html', {'products': products})

def Air_conditionar_products(request):
    products = Product.objects.filter(category__name='Air_conditionar')
    return render(request, 'Air_conditionar.html', {'products': products}) 

def watch_products(request):
    products = Product.objects.filter(category__name='watch')
    return render(request, 'watch.html', {'products': products})

def laptop_products(request):
    products = Product.objects.filter(category__name='laptop')
    return render(request, 'laptop.html', {'products': products})
def search(request):
    searchTerm = request.GET.get('searchTerm')
    if searchTerm:
        products = Product.objects.filter(name__icontains=searchTerm)
    else:
        products = Product.objects.all()  # Show all products if no search term

    return render(request, 'search.html', {'products': products, 'searchTerm': searchTerm})

# 

@login_required
def place_order(request, cart_id):
    customer = request.user
    cart_items = Cart.objects.filter(user=customer)
    
    # Check if the cart is empty
    if not cart_items.exists():
        return HttpResponse('Cart is empty')

    # If the form is submitted (POST request)
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Check if address and phone are provided
        if not address or not phone:
            return HttpResponse('Please provide both address and phone number.')

        orders = []
        
        # Loop through the cart items and place the order for the specified cart_id
        for item in cart_items:
            if item.id == cart_id:
                order = Order(
                    product=item.product,
                    customer=customer,
                    cart_item_ids=str(item.id),
                    quantity=item.quantity,
                    price=item.product.price,
                    address=address,
                    phone=phone,
                )
                order.save()
                orders.append(order)
                item.delete()

        # Redirect to orders page after successful order
        return redirect('orders')

    # If it's a GET request, show the address and phone form
    return render(request, 'place_order.html', {'cart_id': cart_id})


def orders(request):
    # Check if user is authenticated (logged in)
    if request.user.is_authenticated:
        # Get the orders for the logged-in user
        orders1 = Order.objects.filter(customer=request.user)
        return render(request, 'orders.html', {'orders': orders1})
    else:
       
        return redirect('loginaccount')  # Redirect to login page or another appropriate page

def single_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    return render(request, 'product_page.html', {'product': product})

from django.conf import settings
import stripe
# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY



import stripe
from django.conf import settings
from django.shortcuts import render, redirect


stripe.api_key = settings.STRIPE_SECRET_KEY


plan=0
def checkout_session(request, plan_id):
    data = get_object_or_404(Order, id=plan_id)
    plan=data.id

    # Stripe expects the price in the smallest currency unit (paise for INR),
    # so we multiply the price by 100.
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': data.product.name,
                },
                'unit_amount': int(data.price  ),  # Multiply by 100 to convert to paise
            },
            'quantity': data.quantity,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/pay_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/pay_cancel',
        client_reference_id=plan_id
    )
    return redirect(session.url, code=303)


import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY  # Ensure Stripe is initialized

def pay_success(request):
    # Get session_id from the query params
    email(request)
    return redirect('mail')

    


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404

# def send_bill(request, order_id):
   
def pay_cancel(request):
    return redirect('orders')


def createreview(request, movie_id):
    product_ = get_object_or_404(Product, id=movie_id)  # Get the product object by id
    
    if request.method == 'GET':
        # Render the create review page
        return render(request, 'createreview.html', {'product': product_})
    
    else:
        try:
            # Get the review text from POST data
            myreview = request.POST.get('myreview')
            if not myreview:
                raise ValueError("Review cannot be empty")
            
            # Create a new Review object
            newReview = Review()
            newReview.product = product_  # Correct assignment of product
            newReview.user = request.user  # Set the review's author
            newReview.text = myreview     # Set the review content
            
            # Save the review to the database
            newReview.save()
            
          
            return redirect('product_detail',newReview.product.id)
        
        except ValueError:
            # Handle error in case of empty or bad review
            return render(request, 'createreview.html', {'product': product_, 'error': 'Bad data passed in'})

def updatereview(request,review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'GET':
        return render(request,'updatereview.html',{'review':review})
    else:
        try:
            review.text = request.POST.get('myreview')
            review.save()
            return redirect('product_detail',review.product.id)
        except ValueError:
            return render(request,'updatereview.html',{'error':'Bad data passed in'})


def deletereview(request,review_id):
    review = get_object_or_404(Review, pk=review_id,user=request.user)
    review.delete()
    return redirect('product_detail', review.product.id)


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
def complain(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Validate form data
        if not name or not email or not subject or not message:
            messages.error(request, "All fields are required!")
            return render(request, 'complain.html')

        # Prepare the email message
        data = {'name': name, 'email': email, 'subject': subject, 'message': message}
        
        # Call complain_mail and check the result
        if complain_mail(request, data):
            return redirect('complain')  # Redirect on success
        else:
            return render(request, 'complain.html')  # Render form again on failure

    return render(request, 'complain.html')

