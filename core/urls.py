from django.urls import path
from django.views.generic.base import View
from .views import (
    Login,
    BookDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_book_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    CategoryList,
    # go_to_gateway_view
)

app_name = 'core'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
	path('category/<slug:slug>', CategoryList.as_view(), name="category"),
	path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="category"),

    path('product/<int:pk>', BookDetailView.as_view(), name='product'),

    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-book-from-cart/<slug>/', remove_single_book_from_cart,
         name='remove-single-book-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    # path('go_to_gateway/', go_to_gateway_view, name='go_to_gateway'),

]
