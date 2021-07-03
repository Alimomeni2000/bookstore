from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db.models.base import ModelBase
from django.forms.fields import CharField, EmailField
from django.forms.widgets import PasswordInput
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import message

PAYMENT_CHOICES = (
    ('S', 'ای دی پی'),
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_city=forms.CharField( required=False)
    shipping_state=forms.CharField( required=False)

    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_city=forms.CharField( required=False)
    billing_state=forms.CharField( required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'کد تخفیف',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
