from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from restaurant.models import Food, Category, Employee, About, Contact, Address, History
from order.models import Order
from .mixins import SuperUserAccessMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import User
from .forms import ProfileForm, SignUpForm
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


class Home(SuperUserAccessMixin, ListView):
    model = Food
    template_name = 'registration/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['orders'] = Order.objects.all()[0:5]
        context['foods'] = Food.objects.all()[0:5]
        return context
    

class Profile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk) 

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')


class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')


class Register(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'activate your account'
        message = render_to_string('registration/activate_Account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return HttpResponse('activation link was sent to your email. <a href="/login">ورود</a>')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('your account is active now. for login :‌ <a href="/login">click</a>.')
    else:
        return HttpResponse('activation link was expired!! <a href="/login"> try again.</a>')


# food crud

class FoodList(SuperUserAccessMixin, ListView):
    template_name = 'registration/models/food_list.html'
    model = Food


class FoodCreate(SuperUserAccessMixin, CreateView):
    model = Food
    template_name = 'registration/models/food_create_update.html' 
    fields = ('name', 'slug', 'image', 'price', 'description', 'category', 'available')
    success_url = reverse_lazy('account:food_list')


class FoodUpdate(SuperUserAccessMixin, UpdateView):
    model = Food
    template_name = 'registration/models/food_create_update.html' 
    fields = ('name', 'slug', 'image', 'price', 'description', 'category', 'available')
    success_url = reverse_lazy('account:food_list')


class FoodDelete(SuperUserAccessMixin, DeleteView):
    model = Food
    success_url = reverse_lazy('account:food_list')
    template_name = 'registration/models/food_confirm_delete.html'
    

# category crud
class CategoryList(SuperUserAccessMixin, ListView):
    template_name = 'registration/models/category_list.html'
    model = Category


class CategoryCreate(SuperUserAccessMixin, CreateView):
    model = Category
    template_name = 'registration/models/category_create_update.html' 
    fields = ('name', 'slug')
    success_url = reverse_lazy('account:category_list')


class CategoryUpdate(SuperUserAccessMixin, UpdateView):
    model = Category
    template_name = 'registration/models/category_create_update.html' 
    fields = ('name', 'slug')
    success_url = reverse_lazy('account:category_list')


class CategoryDelete(SuperUserAccessMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('account:category_list')
    template_name = 'registration/models/category_confirm_delete.html'
    

# employee crud
class EmployeeList(SuperUserAccessMixin, ListView):
    template_name = 'registration/models/employee_list.html'
    model = Employee


class EmployeeCreate(SuperUserAccessMixin, CreateView):
    model = Employee
    template_name = 'registration/models/employee_create_update.html' 
    fields = ('first_name', 'last_name', 'image', 'position', 
            'description', 'instagram', 'tweeter', 'facebook', 'youtube')
    success_url = reverse_lazy('account:employee_list')


class EmployeeUpdate(SuperUserAccessMixin, UpdateView):
    model = Employee
    template_name = 'registration/models/employee_create_update.html' 
    fields = ('first_name', 'last_name', 'image', 'position', 
            'description', 'instagram', 'tweeter', 'facebook', 'youtube')

    success_url = reverse_lazy('account:employee_list')


class EmployeeDelete(SuperUserAccessMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('account:employee_list')
    template_name = 'registration/models/employee_confirm_delete.html'
    

# about crud
class AboutCreate(SuperUserAccessMixin, CreateView):
    model = About
    template_name = 'registration/models/about_create_update.html' 
    fields = ('description', )
    success_url = reverse_lazy('account:about_update', kwargs={'pk': '1'})


class AboutUpdate(SuperUserAccessMixin, UpdateView):
    model = About
    template_name = 'registration/models/about_create_update.html' 
    fields = ('description', )
    success_url = reverse_lazy('account:about_update', kwargs={'pk': '1'})


# contact crud
class ContactList(SuperUserAccessMixin, ListView):
    template_name = 'registration/models/contact_list.html'
    model = Contact


class ContactDetail(SuperUserAccessMixin, DetailView):
    model = Contact
    template_name = 'registration/models/contact_detail.html'


class ContactDelete(SuperUserAccessMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('account:contact_list')
    template_name = 'registration/models/contact_confirm_delete.html'
    

# address crud
class AddressCreate(SuperUserAccessMixin, CreateView):
    model = Address
    template_name = 'registration/models/address_create_update.html' 
    fields = ('description', 'phone_number', 'email', 
                'tweeter', 'facebook', 'instagram')
    success_url = reverse_lazy('account:address_update', kwargs={'pk': '1'})


class AddressUpdate(SuperUserAccessMixin, UpdateView):
    model = Address
    template_name = 'registration/models/address_create_update.html' 
    fields = ('description', 'phone_number', 'email', 
                'tweeter', 'facebook', 'instagram')
    success_url = reverse_lazy('account:address_update', kwargs={'pk': '1'})


# history crud
class HistoryCreate(SuperUserAccessMixin, CreateView):
    model = History
    template_name = 'registration/models/history_create_update.html' 
    fields = ('description', )
    success_url = reverse_lazy('account:history_update', kwargs={'pk': '1'})


class HistoryUpdate(SuperUserAccessMixin, UpdateView):
    model = History
    template_name = 'registration/models/history_create_update.html' 
    fields = ('description', )
    success_url = reverse_lazy('account:history_update', kwargs={'pk': '1'})


class OrderList(SuperUserAccessMixin, ListView):
    model = Order
    template_name = 'registration/models/order_list.html'
    

class UserOrderList(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'registration/models/user_order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)




    
