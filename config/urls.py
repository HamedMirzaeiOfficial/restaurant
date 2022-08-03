"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account.views import Login, Register, activate
from django.contrib.auth.views import PasswordChangeForm

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'), 
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('accounts/', include('account.urls', namespace='account')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('coupon/', include('coupon.urls', namespace='coupon')),
    path('order/', include('order.urls', namespace='order')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('', include('restaurant.urls', namespace='restaurant')), 
    path('tinymce/', include('tinymce.urls')),
    
] 

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)