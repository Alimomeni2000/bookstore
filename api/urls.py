from django.urls import path
from .views import (
    BookList,
    BookDetail,
    UserList,
    UserDetail,

 
)

app_name = 'api'

urlpatterns = [
    path('', BookList.as_view(), name='list'),
    path('<int:pk>', BookDetail.as_view(), name='detail'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetail.as_view(), name='user-detail'),

]



# urlpatterns += [
#     path('api/checkout/', CheckoutView.as_view(), name='checkout'),
#     # path('api/order-summary/', OrderSummaryView.as_view(), name='order-summary'),
# 	# path('api/category/<slug:slug>', CategoryList.as_view(), name="category"),
# 	# path('api/category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="category"),

#     path('api/product/<int:pk>', BookDetailView.as_view(), name='product'),

#     path('api/add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
#     path('api/add-coupon/', AddCouponView.as_view(), name='add-coupon'),
#     path('api/remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
#     path('api/remove-book-from-cart/<slug>/', remove_single_book_from_cart,
#          name='remove-single-book-from-cart'),
#     path('api/payment/<payment_option>/', PaymentView.as_view(), name='payment'),
#     path('api/request-refund/', RequestRefundView.as_view(), name='request-refund'),
#     # path('go_to_gateway/', go_to_gateway_view, name='go_to_gateway'),

# ]
