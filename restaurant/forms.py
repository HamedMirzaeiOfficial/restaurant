from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        # first_name = 'نام...'
        # message = 'پیام خود را بنویسید...'
        # first_name_label = 'نام'
        # email_label = 'ایمیل'
        # message_label = 'پیام'

        model = Contact
        fields = ('name', 'email', 'message')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ian somerholder'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'iansomer@gmail.com'}), 
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'leave your message for us...'}) 
        }