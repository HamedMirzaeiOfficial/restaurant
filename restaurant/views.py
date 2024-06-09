import imp
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Category, Food, Employee, About, History, Contact, Address
from .forms import ContactForm
from django.contrib import messages


class HomeView(ListView):
    model = Food
    template_name = 'restaurant/home.html'
    context_object_name = 'foods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['foods'] = Food.objects_available.all()

        if self.kwargs.get('slug'):
            context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])
            context['foods'] = Food.objects_available.filter(category=context['category'])
            context['active'] = True
           
        return context

class AboutView(ListView):
    model = Employee
    template_name = 'restaurant/about.html'
    context_object_name = 'employees'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.get(pk=1)
        context['history'] = History.objects.get(pk=1)
        context['active'] = True

        return context

class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'restaurant/contact.html'

    def get_success_url(self) -> str:
        success_message = 'your message was sent to admin.'
        messages.success(self.request, success_message)
        return reverse('restaurant:contact')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['address'] = Address.objects.get(pk=1)
        return context