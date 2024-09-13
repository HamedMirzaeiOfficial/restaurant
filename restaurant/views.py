import imp
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import Category, Food, Employee, About, History, Contact, Address
from .forms import ContactForm
from django.contrib import messages
from django.http import JsonResponse


class HomeView(ListView):
    model = Food
    template_name = 'restaurant/home.html'
    context_object_name = 'foods'
    paginate_by = 100  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryProductListView(ListView):
    model = Food
    context_object_name = 'foods'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug == 'all':
            return Food.objects.all()
        category = get_object_or_404(Category, slug=slug)
        return Food.objects.filter(category=category)

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            foods = context['foods']
            products = [{'id': food.id, 'name': food.name, 'image': food.image.url, 'description': food.description, 'price': food.price} for food in foods]
            return JsonResponse({'products': products})
        return super().render_to_response(context, **response_kwargs)

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