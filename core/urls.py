from django.urls import path
from django.views.generic.base import View
from .views import (
    # Login,
    BookDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_book_from_cart,
    contact,
    about,
    # PaymentView,
    AddCouponView,
    CategoryList,
    SearchList,

    # go_to_gateway_view
)
# from api.views import checkout
app_name = 'core'

urlpatterns = [
    # path('login/', Login.as_view(), name='login'),
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    # path('checkout/', checkout, name='checkout'),

    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
	path('category/<slug:slug>', CategoryList.as_view(), name="category"),
	path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="category"),
    path('search/', SearchList.as_view(), name="search"),
	path('search/page/<int:page>', SearchList.as_view(), name="search"),
    path('product/<int:pk>', BookDetailView.as_view(), name='product'),

    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('contact_us', contact, name='contact'),
    path('about', about, name='about'),

    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-book-from-cart/<slug>/', remove_single_book_from_cart,
         name='remove-single-book-from-cart'),

]
