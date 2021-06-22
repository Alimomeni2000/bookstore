from django import forms
from django.conf import settings
from core.models import Order, UserProfile,Refund
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.fields['username'].disabled=True
        self.fields['email'].disabled=True

    class Meta:
        model= User
        fields = ['username','email','first_name','last_name',]

class UserProfileForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        self.fields['user'].disabled=True
        self.fields['user'].disabled=True

    class Meta:
        model= UserProfile
        fields = ['user','stripe_customer_id','one_click_purchasing',]

class RefundForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(RefundForm,self).__init__(*args,**kwargs)
        self.fields['order'].disabled=True
        self.fields['reason'].disabled=True
        self.fields['email'].disabled=True

    class Meta:
        model= Refund
        fields = ['order','reason','accepted','email']


class OrderForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        
        super(OrderForm,self).__init__(*args,**kwargs)
        
        self.fields['user'].disabled=True
        self.fields['ref_code'].disabled=True
        self.fields['books'].disabled=True
        self.fields['ordered_date'].disabled=True
        self.fields['shipping_address'].disabled=True
        self.fields['billing_address'].disabled=True

        # self.fields['ordered'].disabled=True
        self.fields['payment'].disabled=True
        self.fields['coupon'].disabled=True
        self.fields['refund_requested'].disabled=True


    class Meta:
        model= Order
        fields = "__all__"