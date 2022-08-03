from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from order.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name',
                    'email', 'address', 'postal_code',
                    'city', 'additional_information', 
                    'billing_status', 'created', 'updated',]

    list_filter = ['billing_status', 'created', 'updated']
    inlines = [OrderItemInline]