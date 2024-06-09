from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ian somerholder'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'iansomer@gmail.com'}), 
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'leave your message for us...'}) 
        }