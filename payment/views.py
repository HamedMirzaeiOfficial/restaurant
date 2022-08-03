from django.views import View
from django.shortcuts import render, redirect
from .zarinpal import zpal_request_handler, zpal_payment_checker
from django.conf import settings
from order.models import Order
from django.shortcuts import get_object_or_404
from cart.cart import Cart

class PaymentView(View):
    template_name = 'payment/process.html'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=request.session['order_id'])
        return render(request, self.template_name, {'order': order})   
    

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=request.session['order_id'])
        payment_link, authority = zpal_request_handler(settings.ZARINPAL['merchant_id'], order.get_total_cost_after_discount(),
                                                            'payment for cart', order.email, order.phone, 
                                                             settings.ZARINPAL['gateway_callback_url'])
        
        if payment_link is not None:
            return redirect(payment_link)

        return render(request, self.template_name)



class VerifyView(View):
    template_name = 'payment/callback.html'
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=request.session['order_id'])
        authority = request.GET.get('Authority')
        is_paid, ref_id = zpal_payment_checker(settings.ZARINPAL['merchant_id'], order.get_total_cost_after_discount(), authority)

        if is_paid:
            order.billing_status = True
            order.total_paid = order.get_total_cost_after_discount()
            order.save()

        return render(request, self.template_name, {'is_paid': is_paid, 'ref_id': ref_id})
