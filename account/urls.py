
from django.contrib.auth import views
from django.urls import path
from .views import (
    Profile,
    BookList,
    BookCreate,
    BookUpdate,
    BookDelete,
    CouponList,
    CouponCreate,
    CouponUpdate,
    CouponDelete,
    CategoryList,
    CategoryCreate,
    CategoryUpdate,
    CategoryDelete,
    OrderList,
    OrderUpdate,
    OrderDelete,
    UserList,
    # UserCreate,
    UserUpdate,
    UserDelete,
    RefundList,
    RefundCreate,
    RefundUpdate,
    RefundDelete,
)
from django.contrib.auth.views import LoginView

app_name='account'

urlpatterns = [
    path('login/',LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += [
    path('',Profile.as_view(),name='profile'),
    path('book/list',BookList.as_view(),name='book-list'),
    path('book/create',BookCreate.as_view(),name='book-create'),
    path('book/update/<int:pk>',BookUpdate.as_view(),name='book-update'),
    path('book/delete/<int:pk>',BookDelete.as_view(),name='book-delete'),
    path('coupon/list',CouponList.as_view(),name='coupon-list'),
    path('coupon/create',CouponCreate.as_view(),name='coupon-create'),
    path('coupon/update/<int:pk>',CouponUpdate.as_view(),name='coupon-update'),
    path('coupon/delete/<int:pk>',CouponDelete.as_view(),name='coupon-delete'),
    path('category/list',CategoryList.as_view(),name='category-list'),
    path('category/create',CategoryCreate.as_view(),name='category-create'),
    path('category/update/<int:pk>',CategoryUpdate.as_view(),name='category-update'),
    path('category/delete/<int:pk>',CategoryDelete.as_view(),name='category-delete'),
    path('order/list',OrderList.as_view(),name='order-list'),
    path('order/update/<int:pk>',OrderUpdate.as_view(),name='order-update'),
    path('order/delete/<int:pk>',OrderDelete.as_view(),name='order-delete'),
    path('user/list',UserList.as_view(),name='user-list'),
    path('user/update/<int:pk>',UserUpdate.as_view(),name='user-update'),
    path('user/delete/<int:pk>',UserDelete.as_view(),name='user-delete'),
    path('refund/list',RefundList.as_view(),name='refund-list'),
    path('refund/create',RefundCreate.as_view(),name='refund-create'),
    path('refund/update/<int:pk>',RefundUpdate.as_view(),name='refund-update'),
    path('refund/delete/<int:pk>',RefundDelete.as_view(),name='refund-delete'),

]