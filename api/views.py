
from core.views import BookDetailView
from django.shortcuts import render
from .serializers import BookSerializer, UserSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.contrib.auth.models import Permission, User
from core.models import Book
from .permissions import (
    IsAuthorOrReadOnly,
    IsStaffOrReadOnly,
    IsSuperUser,
    IsSuperUserOrStaffReadOnly,
)
# Create your views here.


class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
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
