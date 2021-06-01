from django.urls import path
from .views import (
    ItemList,
    ItemDetail,
    UserList,
    UserDetail,
)

app_name = 'api'

urlpatterns = [
    path('', ItemList.as_view(), name='list'),
    path('<int:pk>', ItemDetail.as_view(), name='detail'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>', UserDetail.as_view(), name='user-detail'),

]
