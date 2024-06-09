from django.urls import path
from . import views

app_name = 'account'


urlpatterns = [
    path('', views.Home.as_view(), name='home'), 
    path('profile/', views.Profile.as_view(), name='profile'),   

    path('food/list/', views.FoodList.as_view(), name='food_list'), 
    path('food/create/', views.FoodCreate.as_view(), name='food_create'), 
    path('food/update/<int:pk>/', views.FoodUpdate.as_view(), name='food_update'),
    path('food/delete/<int:pk>/', views.FoodDelete.as_view(), name='food_delete'),

    path('category/list/', views.CategoryList.as_view(), name='category_list'), 
    path('category/create/', views.CategoryCreate.as_view(), name='category_create'), 
    path('category/update/<int:pk>/', views.CategoryUpdate.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', views.CategoryDelete.as_view(), name='category_delete'),
    
    path('employee/list/', views.EmployeeList.as_view(), name='employee_list'), 
    path('employee/create/', views.EmployeeCreate.as_view(), name='employee_create'), 
    path('employee/update/<int:pk>/', views.EmployeeUpdate.as_view(), name='employee_update'),
    path('employee/delete/<int:pk>/', views.EmployeeDelete.as_view(), name='employee_delete'),
    
    path('about/create/', views.AboutCreate.as_view(), name='about_create'), 
    path('about/create/<int:pk>/', views.AboutUpdate.as_view(), name='about_update'),

    path('contact/list/', views.ContactList.as_view(), name='contact_list'), 
    path('contact/detail/<int:pk>/', views.ContactDetail.as_view(), name='contact_detail'), 
    path('contact/delete/<int:pk>/', views.ContactDelete.as_view(), name='contact_delete'),
    path('contact/detail/<int:pk>/', views.ContactDetail.as_view(), name='contact_detail'), 

    path('address/create/', views.AddressCreate.as_view(), name='address_create'), 
    path('address/create/<int:pk>/', views.AddressUpdate.as_view(), name='address_update'),

    path('history/create/', views.HistoryCreate.as_view(), name='history_create'), 
    path('history/create/<int:pk>/', views.HistoryUpdate.as_view(), name='history_update'),

    path('order/list/', views.OrderList.as_view(), name='order_list'),
    path('user_order/list/', views.UserOrderList.as_view(), name='user_order_list'),    
]
