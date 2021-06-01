from django.db.models.base import ModelState
<<<<<<< HEAD
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
=======
from rest_framework import serializers
from core.models import Item


class ItemSerializer(serializers.ModelSerializers):
    class Meta:
        model = Item
        fields = (
            'title',
            'price',
            'discount_price',
>>>>>>> 033ceea607ac63bc133e7d16a8aed6e5cbe67b43
            'category',
            'label',
            'slug',
            'description',
            'image',
            'imageslide',
        )
<<<<<<< HEAD


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
=======
>>>>>>> 033ceea607ac63bc133e7d16a8aed6e5cbe67b43
