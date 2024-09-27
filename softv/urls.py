
from . import mail_work
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import add_to_cart, cart_view,remove_from_cart,liked_view,add_to_liked,remove_from_liked,tv_products,phone_products,speaker_products,laptop_products
from .views import orders
urlpatterns = [
    path("",views.index,name="index"),
    # path('email/', views.send_email_to_client, name='send_email_to_client'),
    path('/contact',views.complain,name='complain'),
    path('accounts/',include('accounts.urls')),
    path('about/',views.about,name="about"),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('remove-from-cart/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('remove-from-order/<int:item_id>/',views.remove_from_order, name='remove_from_order'),
    

    path('add-to-liked/<int:product_id>/', add_to_liked, name='add_to_liked'),
    path('liked/', liked_view, name='liked'),
    path('remove-from-liked/<int:item_id>/',remove_from_liked, name='remove_from_liked'),
    path('login/', views.login_view, name='login'),      #  path('toggle_like/<int:product_id>/', views.toggle_like, name='toggle_like'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('tv/', views.tv_products, name='tv_products'),
    path('mobile-cat/', views.mobile, name='mobile'),
    path('tv-cat/', views.tv, name='tv'),
    path('watch-cat/', views.watch, name='mobwatchile'),
    path('ac-cat/', views.ac, name='ac'),
    path('speaker-cat/', views.speaker, name='speaker'),
    path('laptop-cat/', views.laptop, name='laptop'),


    path('Air_conditionar/', views.Air_conditionar_products, name='ac'),


    path('phone/', views.phone_products, name='phone_products'),
    path('speaker/', views.speaker_products, name='speaker_products'),
    path('laptop/', views.laptop_products, name='laptop_products'),
    path('place_order/<int:cart_id>/', views.place_order, name='place_order'),
    path('orders/', orders, name='orders'),
    # path( 'checkout_session/<int:id>' , views.checkout_session, name= 'checkout_session' ) ,
    path('checkout_session/<int:plan_id>',views.checkout_session,name='checkout_session'),
	path('pay_success/',views.pay_success,name='pay_success'),
	path('pay_cancel/',views.pay_cancel,name='pay_cancel'),
	path('inc/<int:id>',views.increase,name='increase'),
	path('dec/<int:id>',views.decrease,name='decrease'),
    path('detail/<int:movie_id>/',views.createreview,name='createreview'),
    path('review/<int:review_id>',views.updatereview,name='updatereview'),
    path('review/<int:review_id>/',views.deletereview,name='deletereview'),
    path('search/', views.search, name='search'),
    path('watch/', views.watch_products, name='watch_products'),




    # path('bill/',views.bill,name='bill'),
    path('mail/',mail_work.email,name='mail')
    # path('bill/<int:order_id>/', views.send_bill, name='send_bill'),    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
