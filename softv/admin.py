
from django.contrib import admin
from . models import Product,Cart,Category,Order,Liked,Review
from django.template.loader import render_to_string
from django.contrib.auth.models import User


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Liked)
admin.site.register(Review)
admin.site.register(Cart)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'quantity',
                    'price', 'address', 'phone', 'date', 'status','payment')
    actions = ['confirm_orders']
    list_filter = ('status', 'date', 'customer')

    def confirm_orders(self, request, queryset):
        customer_orders = {}

        for order in queryset:
            order.status = True
            order.save()
            cart_item_ids = order.cart_item_ids.split(',')
            Cart.objects.filter(id__in=cart_item_ids).delete()

            if order.customer.id not in customer_orders:
                customer_orders[order.customer.id] = []

            customer_orders[order.customer.id].append(order)

        for customer_id, orders in customer_orders.items():
            customer = User.objects.get(id=customer_id)
            all_confirmed = Order.objects.filter(
                customer=customer, status=False).count() == 0

            # if all_confirmed:
            #     self.send_confirmation_email(customer, orders)

        self.message_user(
            request, "Selected orders have been confirmed and cart items removed.")
    confirm_orders.short_description = 'Confirm selected orders'

    # def send_confirmation_email(self, customer, orders):
    #     subject = 'All Your Orders are Confirmed'

    #     address = orders[0].address if orders else "No Address"

    #     message_html = render_to_string('order_confirmation_email.html', {
    #         'customer': customer,
    #         'orders': orders,
    #         'address': address,
    #     })

    #     recipient_list = ['your-email@gmail.com']

    #     send_html_email(subject, message_html, recipient_list)


admin.site.register(Order, OrderAdmin)

