from django.db import models
from .zarinpal import zpal_request_handler, zpal_payment_checker
import uuid
from django.conf import settings


class Gateway(models.Model):

    """
        Save Gateway name and credentials to the database and use them to handle payments. 
    """

    # CAUTION: do not change bellow function name
    FUNCTION_SAMAN = 'saman'
    FUNCTION_SHAPARAK = 'shaparak'
    FUNCTION_FINOTECH = 'finotech'
    FUNCTION_ZARRINPAL = 'zarrinpal'
    FUNCTION_PARSIAN = 'parsian'
    GATEWAY_FUNCTIONS = (
        (FUNCTION_SAMAN, 'Saman'), 
        (FUNCTION_SHAPARAK, 'Shaparak'), 
        (FUNCTION_FINOTECH, 'Finotech'), 
        (FUNCTION_ZARRINPAL, 'Zarrinpal'), 
        (FUNCTION_PARSIAN, 'Parsian'), 
    )


    title = models.CharField(max_length=100, verbose_name=' gateway title')
    gateway_request_url = models.CharField(max_length=150, verbose_name='request url', null=True, blank=True)
    gateway_verify_url = models.CharField(max_length=150, verbose_name='verify url', null=True, blank=True)
    gateway_code = models.CharField(max_length=12, verbose_name='gateway code', choices=GATEWAY_FUNCTIONS)
    is_enable = models.BooleanField(verbose_name='is enable', default=True)
    auth_data = models.TextField(verbose_name='auth data', null=True, blank=True)


    class Meta:
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'
    

    def __str__(self):
        return self.title


    def get_request_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None, 
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_FINOTECH: None, 
            self.FUNCTION_ZARRINPAL: zpal_request_handler,
            self.FUNCTION_PARSIAN: None,
        }

        return handlers[self.gateway_code]


    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None, 
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_FINOTECH: None, 
            self.FUNCTION_ZARRINPAL: zpal_payment_checker,
            self.FUNCTION_PARSIAN: None,
        }

        return handlers[self.gateway_code]


    @property
    def credentials(self):
        return json.loads(self.auth_data)





class Payment(models.Model):
        invoice_number = models.UUIDField(verbose_name='invoice number', unique=True, default=uuid.uuid4)
        amount = models.PositiveIntegerField(verbose_name='payment amount', editable=True)
        gateway = models.ForeignKey(Gateway, related_name='payments', null=True, blank=True,
                                    verbose_name='gateway', on_delete=models.CASCADE)
        is_paid = models.BooleanField(verbose_name='is paid status', default=False)
        payment_log = models.TimeField(verbose_name='logs', blank=True)
        user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True , on_delete=models.SET_NULL)
        authority = models.CharField(max_length=64, verbose_name='authority', blank=True)


        class Meta:
            verbose_name = 'Payment'
            verbose_name_plural = 'Payments'


        def __str__(self):
            return self.invoice_number.hex

        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._b_is_paid = self.is_paid


        @property
        def bank_page(self):
            handler = self.gateway.get_request_handler()
            if handler is not None:
                return handler(self.gateway, self)


        @property
        def title(self):
            return 'Instant payment'


        def status_changed(self):
            return self.is_paid != self._b_is_paid


        def verify(self, data):
            handler = self.gateway.get_verify_handler()
            if not self.is_paid and handler is not None:
                handler(self, data)
            return self.is_paid 


        def get_gateway(self):
            gateway = Gateway.objects.filter(is_enable=True).first()
            return gateway.gateway_code


        def save_log(self, data, scope='Request handler', save=True):
            generated_log = "[{}][{}] {}\n".format(timezone.now(), scope, data)
            if self.payment_log != '':
                self.payment_log += generated_log
            else:
                self.payment_log = generated_log
  
            if save:
                self.save()
                
