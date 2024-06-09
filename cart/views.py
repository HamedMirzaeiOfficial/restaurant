from django.shortcuts import render, redirect
from restaurant.models import Food
from django.contrib.auth.decorators import login_required
from .cart import Cart
from coupon.forms import CouponApplyForm


@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = Food.objects.get(id=id)
    cart.add(product=product)
    return redirect("restaurant:home")

@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Food.objects.get(id=id)
    cart.remove(product)
    return redirect("cart:cart_detail")

@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Food.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart:cart_detail")

@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Food.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart:cart_detail")

@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart:cart_detail")

@login_required
def cart_detail(request):
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/cart_detail.html', {'coupon_apply_form': coupon_apply_form})