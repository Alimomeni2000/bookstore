from django.db.models.base import ModelState
from core.models import Item
from rest_framework import serializers
from django.contrib.auth.models import User


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'title',
            'price',
            'discount_price',
            "get_absolute_url",
            'category',
            'label',
            'slug',
            'description',
            'image',
            'imageslide',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
