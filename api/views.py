from django.urls import reverse

from core.models import Book, OrderBook, Order

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .serializers import BookSerializer, UserSerializer
from rest_framework import generics
# .ListAPIView, RetrieveAPIView,api_view
# from django.contrib.auth.models import AbstractUser
from core.models import Book
from .permissions import (
    IsAuthorOrReadOnly,
    IsStaffOrReadOnly,
    IsSuperUser,
    IsSuperUserOrStaffReadOnly,
)
from core.models import Book, OrderBook, Order, SlidShow, Address, Payment, Coupon, Refund, UserProfile,Category
from .serializers import OrderSerializer 
# Create your views here.
# class User(AbstractUser):
#     pass

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsStaffOrReadOnly, IsAuthorOrReadOnly)

from rest_framework.decorators import api_view



@api_view(['GET', 'POST', 'DELETE'])

@login_required
def add_to_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    order_book, created = OrderBook.objects.get_or_create(
        book=book,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order book is in the order
        if order.books.filter(book__slug=book.slug).exists():
            order_book.quantity += 1
            order_book.save()
            messages.info(request, "تعداد کتاب ها آپدیت شد.")
            return redirect("core:order-summary")
        else:
            order.books.add(order_book)
            messages.info(request, "این کتاب به سبد خرید شما اضافه شد.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.books.add(order_book)
        messages.info(request, "این کتاب به سبد خرید شما اضافه شد.")
        return redirect("core:order-summary")
        
@api_view(['GET', 'POST', 'DELETE'])

@login_required
def remove_from_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order book is in the order
        if order.books.filter(book__slug=book.slug).exists():
            order_book = OrderBook.objects.filter(
                book=book,
                user=request.user,
                ordered=False
            )[0]
            order.books.remove(order_book)
            order_book.delete()
            
        # else:
            # messages.info(request, "این کتاب در سبد خرید شما وجود ندارد .")
            # return redirect("core:product", slug=slug)
    # else:
    #     messages.info(request, "شما سفارش فعالی ندارید.")
    #     return redirect("core:product", slug=slug)

@api_view(['GET', 'POST', 'DELETE'])

@login_required
def remove_single_book_from_cart(request, slug):
    book = get_object_or_404(Book, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order book is in the order
        if order.books.filter(book__slug=book.slug).exists():
            order_book = OrderBook.objects.filter(
                book=book,
                user=request.user,
                ordered=False
            )[0]
            if order_book.quantity > 1:
                order_book.quantity -= 1
                order_book.save()
            else:
                order.books.remove(order_book)
            messages.info(request, "تعداد کتاب ها آپدیت شد.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "این کتاب در سبد خرید شما وجود ندارد ")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "شما سفارش فعالی ندارید. ")
        return redirect("core:product", slug=slug)

@api_view(['GET', 'POST', 'DELETE'])

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "این کد تخفیف وجود ندارد.")
        return redirect("core:checkout")


# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()

#     serializer_class = UserSerializer
#     permission_classes = (IsSuperUserOrStaffReadOnly,)


# class UserDetail(generics.RetrieveAPIView):
#     # queryset = User.objects.all()
#     def get_queryset(self):
#         return User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsSuperUserOrStaffReadOnly,)



# class CategoryDetail(APIView):
#     def get_object(self, category_slug):
#         try:
#             return Category.objects.get(slug=category_slug)
#         except Category.DoesNotExist:
#             raise Http404

#     def get(self, request, category_slug, format=None):
#         category = self.get_object(category_slug)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)


# class Profile(UpdateView):
#     model =User
#     form_class=ProfileForm
#     success_url= reverse_lazy('account:profile')

#     template_name='registration/profile.html'
#     def get_object(self):
#         return User.objects.get(pk=self.request.user.pk)
