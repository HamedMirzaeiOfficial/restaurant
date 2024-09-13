from django.shortcuts import render, redirect
from restaurant.models import Food
from django.contrib.auth.decorators import login_required
from .cart import Cart
from coupon.forms import CouponApplyForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse


@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Food, id=id)
    cart.add(product=product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  
        return JsonResponse({'message': 'Product added to cart!', 'product_name': product.name})
    else:
        messages.success(request, 'Product added to cart!')
        return redirect('restaurant:home')
    
@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = get_object_or_404(Food, id=id)
    cart.remove(product)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Item removed!',
            'cart_total': cart.get_total_price(),
            'cart_discount': cart.get_discount(),
            'cart_total_after_discount': cart.get_total_price_after_discount(),
        })
    messages.success(request, 'Item removed!')
    return redirect("cart:cart_detail")

@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = get_object_or_404(Food, id=id)
    cart.add(product=product)
    
    item_quantity = cart.get_item_quantity(product)
    item_total_price = cart.get_item_total_price(product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Item quantity updated!',
            'item_quantity': item_quantity,
            'item_total': item_total_price,
            'cart_total': cart.get_total_price(),
            'cart_discount': cart.get_discount(),
            'cart_total_after_discount': cart.get_total_price_after_discount(),
        })
    messages.success(request, 'Item quantity updated!')
    return redirect("cart:cart_detail")

@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = get_object_or_404(Food, id=id)
    cart.decrement(product=product)
    
    item_quantity = cart.get_item_quantity(product)
    item_total_price = cart.get_item_total_price(product)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Item quantity updated!',
            'item_quantity': item_quantity,
            'item_total': item_total_price,
            'cart_total': cart.get_total_price(),
            'cart_discount': cart.get_discount(),
            'cart_total_after_discount': cart.get_total_price_after_discount(),
        })
    messages.success(request, 'Item quantity updated!')
    return redirect("cart:cart_detail")

@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'all items removes!')
    return redirect("cart:cart_detail")

@login_required
def cart_detail(request):
    coupon_apply_form = CouponApplyForm()
    return render(request, 'cart/cart_detail.html', {'coupon_apply_form': coupon_apply_form})