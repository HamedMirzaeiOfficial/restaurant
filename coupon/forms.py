from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': '1234ABC'}))
    code.label = 'Promocode'