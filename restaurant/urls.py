from django.urls import path
from . import views


app_name = 'restaurant'


urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'), 
    path('contact/', views.ContactView.as_view(), name='contact'), 
    path('<slug>/', views.HomeView.as_view(), name='home_by_category'),
    path('', views.HomeView.as_view(), name='home'), 
]