from re import A
from django.contrib import admin
from .models import Category, Food, Employee, About, History, Contact, Address


admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Employee)
admin.site.register(About)
admin.site.register(History)
admin.site.register(Contact)
admin.site.register(Address)


