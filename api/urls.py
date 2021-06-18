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
