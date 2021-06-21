from django.db.models.fields import Field
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from core.models import (Book,
                    Coupon,
                    Category,
                    Order ,
                    UserProfile,
                    Refund,
                                        )
from .forms import UserProfileForm,RefundForm,ProfileForm
# Create your views here.

class Profile(UpdateView):
    model =User
    form_class=ProfileForm
    success_url= reverse_lazy('account:profile')

    template_name='registration/profile.html'
    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

class BookList(LoginRequiredMixin,ListView):
    queryset=Book.objects.all()
    template_name='registration/booklist.html'

class BookCreate(LoginRequiredMixin,CreateView):
    model = Book
    fields = "__all__"
    template_name='registration/book-create-update.html'

class BookUpdate(LoginRequiredMixin,UpdateView):
    model = Book
    fields = "__all__"

    template_name='registration/book-create-update.html'


class BookDelete(LoginRequiredMixin,DeleteView):
    model = Book
    success_url= reverse_lazy('account:book-list')
    template_name='registration/book_confirm_delete.html'

class CouponList(LoginRequiredMixin,ListView):
    queryset=Coupon.objects.all()
    template_name='registration/coupon-list.html'

class CouponCreate(LoginRequiredMixin,CreateView):
    model = Coupon
    # fields = ['code','amount']
    fields = "__all__"

    template_name='registration/coupon-create-update.html'

class CouponUpdate(LoginRequiredMixin,UpdateView):
    model = Coupon
    # fields =['code','amount']
    fields = "__all__"

    template_name='registration/coupon-create-update.html'

class CouponDelete(LoginRequiredMixin,DeleteView):
    model = Coupon
    success_url= reverse_lazy('account:coupon-list')
    template_name='registration/coupon_confirm_delete.html'



class CategoryList(LoginRequiredMixin,ListView):
    queryset=Category.objects.all()
    template_name='registration/category-list.html'

class CategoryCreate(LoginRequiredMixin,CreateView):
    model = Category
    fields = "__all__"

    template_name='registration/category-create-update.html'

class CategoryUpdate(LoginRequiredMixin,UpdateView):
    model = Category
    fields = "__all__"

    template_name='registration/category-create-update.html'

class CategoryDelete(LoginRequiredMixin,DeleteView):
    model = Category
    success_url= reverse_lazy('account:category-list')
    template_name='registration/category_confirm_delete.html'



class OrderList(LoginRequiredMixin,ListView):
    template_name='registration/order-list.html'
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)
class OrderUpdate(LoginRequiredMixin,UpdateView):
    model = Order
    fields = "__all__"

    template_name='registration/order-create-update.html'

class OrderDelete(LoginRequiredMixin,DeleteView):
    model = Order
    success_url= reverse_lazy('account:order-list')
    template_name='registration/order_confirm_delete.html'


class UserList(LoginRequiredMixin,ListView):
    queryset=UserProfile.objects.all()
    template_name='registration/user-list.html'

class UserUpdate(LoginRequiredMixin,UpdateView):
    model = UserProfile
    form_class=UserProfileForm
    # fields = "__all__"

    template_name='registration/user-create-update.html'

class UserDelete(LoginRequiredMixin,DeleteView):
    model = UserProfile
    success_url= reverse_lazy('account:user-list')
    template_name='registration/user_confirm_delete.html'




class RefundList(LoginRequiredMixin,ListView):
    queryset=Refund.objects.all()
    template_name='registration/refund-list.html'

class RefundCreate(LoginRequiredMixin,CreateView):
    model = Refund
    fields = "__all__"
    template_name='registration/refund-create-update.html'

class RefundUpdate(LoginRequiredMixin,UpdateView):
    model = Refund
    form_class=RefundForm
    template_name='registration/refund-create-update.html'


class RefundDelete(LoginRequiredMixin,DeleteView):
    model = Refund
    success_url= reverse_lazy('account:refund-list')
    template_name='registration/refund_confirm_delete.html'