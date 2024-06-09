from django.urls import path
from . import views

app_name = 'payment'


urlpatterns = [
    path('process/', views.PaymentView.as_view(), name='process'), 
    path('verify/', views.VerifyView.as_view(), name='verify'), 
]

