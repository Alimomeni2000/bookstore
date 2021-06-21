from django import forms
from django.conf import settings
from core.models import UserProfile,Refund
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
