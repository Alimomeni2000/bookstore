from core.views import ItemDetailView
from django.shortcuts import render
from .serializers import ItemSerializer, UserSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.contrib.auth.models import Permission, User
from core.models import Item
from .permissions import (
    IsAuthorOrReadOnly,
    IsStaffOrReadOnly,
    IsSuperUser,
    IsSuperUserOrStaffReadOnly,
)
# Create your views here.


class ItemList(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetail(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsStaffOrReadOnly, IsAuthorOrReadOnly)


class UserList(ListAPIView):
    queryset = User.objects.all()

    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrStaffReadOnly,)


class UserDetail(RetrieveAPIView):
    # queryset = User.objects.all()
    def get_queryset(self):
        return User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrStaffReadOnly,)
