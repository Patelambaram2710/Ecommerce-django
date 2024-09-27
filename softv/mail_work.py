

from django.template.loader import render_to_string
from django.utils.html import strip_tags
import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string 
from django.utils.html import strip_tags
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Liked ,Order , Review
import os

def email(request) :
     session_id = request.GET.get('session_id')
     if session_id:
        # Retrieve the Stripe session
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            order_id = session.client_reference_id  # This was set during the checkout
            # Fetch the order details using the `order_id` and authenticated user
            order = get_object_or_404(Order, id=order_id, customer=request.user)
            order.payment = True  # Mark payment as completed
            order.save()  # Save the updated order
            # Prepare the context data to pass to the email template
            context = {
                'user': request.user.username,
                'price':order.price,
                'items': order.product.name,  # Assuming you want to show the product in the email
                'total': order.price * order.quantity,
                'quantity':order.quantity

               
            }
            # Render the email content using an HTML template
            subject = "Your Purchase Bill - Order #{}".format(order.id)
            html_message = render_to_string('bill.html', context)  # Correct path for the template
            plain_message = strip_tags(html_message)  # Fallback for non-HTML email clients
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [request.user.email]

            # Create and send the email
            email = EmailMessage(subject, html_message, from_email, recipient_list)
            email.content_subtype = "html"  # Set the email content type to HTML
            email.send()
            return redirect('orders')
        except stripe.error.InvalidRequestError:
                return redirect('orders')
     else:
            return redirect('orders')




def out_of_stock(request):
    products = Product.objects.all()
    out_of_stock_products = []
    owner=os.getenv('OWNER_EMAIL')

    # Loop through all products and check if any are out of stock
    for product in products:
        if product.quantity <= 0:
            out_of_stock_products.append(product)

    if out_of_stock_products:
        # Prepare email to notify the owner
        context = {
            'products': out_of_stock_products,
            'year' : 2004,  # Pass the list of out-of-stock products to the email template
            'user': request.user.username,
        }

        # Set up email details
        subject = "Out of Stock Notification"
        html_message = render_to_string('out_of_stock.html', context)  # Email HTML template
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['bharatsingh87368@gmail.com']  # The owner's email from settings

        # Send the email to the owner
        email = EmailMessage(subject, html_message, from_email, recipient_list)
        email.content_subtype = "html"
        email.send()

    return ""



from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib import messages

def complain_mail(request, data):
    subject = f"Complaint from {data['name']}"
    full_message = f"Name: {data['name']}\nEmail: {data['email']}\n\nMessage:\n{data['message']}"
    
    # Use a fixed email address for the sender (the owner or support email)
    from_email = data['email']  # Replace with your support email
    to_email = ['bharatsingh87368@gmail.com']  # Owner's email

    try:
        email = EmailMessage(
            subject,
            full_message,
            from_email,
            to_email,
        )
        
        # Set the reply-to header to the user's email
        email.reply_to = [data['email']]
        
        email.send(fail_silently=False)
        messages.success(request, "Your complaint has been submitted successfully!")
        return True  # Indicate success
    except Exception as e:
        messages.error(request, f"An error occurred while sending the email: {e}")
        return False  # Indicate failure
