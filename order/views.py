from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order
import uuid

def order_create(request):
    cart = Cart(request)
    order = None
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.order_key = uuid.uuid4().hex
            order.total_paid = 0


            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = order.coupon.discount
                
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])


            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id
            request.session.modified = True

            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
        return render(request, 'order/create_order.html',
                      {'cart': cart, 'form': form, 'order': order})


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders


