from django.urls import path
from . import views


app_name = 'restaurant'


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:slug>/', views.CategoryProductListView.as_view(), name='products_by_category'),
    path('about/', views.AboutView.as_view(), name='about'), 
    path('contact/', views.ContactView.as_view(), name='contact'), 
]