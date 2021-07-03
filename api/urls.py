from django.urls import path
from .views import (
    BookList,
    BookDetail,
    # UserList,
    # UserDetail,
    checkout,
    add_to_cart,
    remove_from_cart,
    remove_single_book_from_cart,
)
from core.views import CheckoutView
app_name = 'api'

urlpatterns = [
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-book-from-cart/<slug>/', remove_single_book_from_cart,
         name='remove-single-book-from-cart'),
    path('', BookList.as_view(), name='list'),
    path('<int:pk>/', BookDetail.as_view(), name='detail'),
    # path('checkout/', checkout, name='checkout'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),


]
