from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm
from cart.cart import Cart  # Assuming Cart is defined in cart/cart.py

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    cart = Cart(request)  # Initialize the cart object

    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            request.session['coupon_id'] = coupon.id
            request.session['coupon_code'] = coupon.code
            message = 'Coupon applied successfully!'
            success = True
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            message = "Coupon doesn't exist!"
            success = False

        # Return total price, discount, and total price after discount in JSON response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success' if success else 'error',
                'message': message,
                'cart_total': cart.get_total_price(),  # Total price
                'cart_discount': cart.get_discount(),  # Discount value
                'cart_total_after_discount': cart.get_total_price_after_discount(),  # Price after discount
            })
    return JsonResponse({'status': 'error', 'message': 'Invalid form submission'})
