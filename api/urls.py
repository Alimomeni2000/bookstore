from django.urls import path
from .views import (
    BookList,
    BookDetail,
    # UserList,
    # UserDetail,
    add_to_cart,
    remove_from_cart,
    remove_single_book_from_cart,
)

app_name = 'api'

urlpatterns = [
    # path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-book-from-cart/<slug>/', remove_single_book_from_cart,
         name='remove-single-book-from-cart'),
    path('', BookList.as_view(), name='list'),
    path('/<int:pk>', BookDetail.as_view(), name='detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),

    # path('users/', UserList.as_view(), name='user-list'),
    # path('users/<int:pk>', UserDetail.as_view(), name='user-detail'),

]
