from django.urls import reverse

from core.models import Book, OrderBook, Order

from rest_framework.decorators import api_view
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from core.forms import CheckoutForm, CouponForm
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer, UserSerializer,CategorySerializer
from rest_framework import generics
from django.http import HttpResponse
from core.models import Book,Address

from core.models import (Book,
    OrderBook,
    Order,
    Coupon,
    Category
    )
from .serializers import (MyOrderSerializer, OrderSerializer,)

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = (IsStaffOrReadOnly, IsAuthorOrReadOnly)



def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid



@api_view(['GET',])

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
            # return messages.info(request, "تعداد کتاب ها آپدیت شد.")
        else:
            order.books.add(order_book)
            # return messages.info(request, "این کتاب به سبد خرید شما اضافه شد.")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.books.add(order_book)
        # return messages.info(request, "این کتاب به سبد خرید شما اضافه شد.")
        
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
            # return messages.info(request, "این کتاب در سبد خرید شما وجود ندارد .")
    # else:
        # return messages.info(request, "شما سفارش فعالی ندارید.")



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
    #         return messages.info(request, "تعداد کتاب ها آپدیت شد.")
    #     else:
    #         return messages.info(request, "این کتاب در سبد خرید شما وجود ندارد ")
    # else:
    #     return messages.info(request, "شما سفارش فعالی ندارید. ")


@api_view(['GET', 'POST', 'DELETE'])
def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "این کد تخفیف وجود ندارد.")
        return redirect("core:checkout")


from rest_framework.decorators import api_view, authentication_classes, permission_classes

from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        get_total = sum(item.get('quantity') * item.get('book').price for item in serializer.validated_data['books'])

        try:
            charge = stripe.Charge.create(
                amount=int(get_total * 100),
                currency='USD',
                description='Charge from Djackets',
            )

            serializer.save(user=request.user, get_total=get_total)

            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user=request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)
