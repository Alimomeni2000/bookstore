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
from core.forms import CheckoutForm, CouponForm, RefundForm
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer, UserSerializer,CategorySerializer
from rest_framework import generics
from django.http import HttpResponse
from core.models import Book
from .permissions import (
    IsAuthorOrReadOnly,
    IsStaffOrReadOnly,
    IsSuperUser,
    IsSuperUserOrStaffReadOnly,
)
from core.models import Book, OrderBook, Order, SlidShow, Address, Payment, Coupon, Refund, UserProfile,Category
from .serializers import OrderSerializer 

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


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "درخواست شما دریافت شد.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "این کتاب وجود ندارد.")
                return redirect("core:request-refund")



class CheckoutView(View):

    permission_classes = (IsAuthenticated,)
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "شما سفارش فعالی ندارید.")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "آدرس پستی پیس فرض در وجود ندارد")
                        return redirect('core:checkout')
                else:
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_city = form.cleaned_data.get(
                        'shipping_city')
                    shipping_state = form.cleaned_data.get(
                        'shipping_state')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1,shipping_city,shipping_state ,shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            city=shipping_city,
                            state=shipping_state,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip_code=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "لطفا همه فیلد های مربوط به آدرس را پر کنید . ")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "آدرس پستی پیس فرض در وجود ندارد")
                        return redirect('core:checkout')
                else:
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_state = form.cleaned_data.get(
                        'billing_state')
                    billing_city = form.cleaned_data.get(
                        'billing_city')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_state,billing_city,billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            city=billing_city,
                            state=billing_state,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip_code=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                        return HttpResponse(order)
                    else:
                        messages.info(
                            self.request, "لطفا همه فیلد های مربوط به آدرس را پر کنید . ")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('go_to_gateway')
                elif payment_option == 'P':
                    return redirect('go_to_gateway')
                else:
                    messages.warning(
                        self.request, "گزینه پرداخت را انتخاب کنید. ")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "شما سفارش فعالی ندارید.")
            return redirect("core:order-summary")


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
