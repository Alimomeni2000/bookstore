from django.db.models.base import ModelState

from core.models import Book
from rest_framework import serializers
from django.contrib.auth.models import User


from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
