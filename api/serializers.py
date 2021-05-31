from django.db.models.base import ModelState
from rest_framework import serializers
from core.models import Item


class ItemSerializer(serializers.ModelSerializers):
    class Meta:
        model = Item
        fields = (
            'title',
            'price',
            'discount_price',
            'category',
            'label',
            'slug',
            'description',
            'image',
            'imageslide',
        )
