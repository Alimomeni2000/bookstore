from django.db.models.base import ModelState

from core.models import Book,Category
from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import OrderBook, Order


from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

from rest_framework import serializers

from core.models import Order, OrderBook


class MyOrderBookSerializer(serializers.ModelSerializer):    
    product = BookSerializer()

 
    class Meta:
        model = OrderBook
        fields = (
            "user",
            "ordered",
            "book",
            "quantity",
        )



class MyOrderSerializer(serializers.ModelSerializer):
    books = MyOrderBookSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "order_code",
            "ref_code",
            "books",
            "ordered_date",
            "shipping_address",
            "billing_address",
            "being_delivered",
            "coupon",
            "refund_requested"
        )
class OrderBookSerializer(serializers.ModelSerializer):    
    class Meta:
        model = OrderBook
        fields = (
            "user",
            "book",
            "quantity",
        )



class OrderSerializer(serializers.ModelSerializer):
    books = OrderBookSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "order_code",
            "ref_code",
            "books",
            "ordered_date",
            "shipping_address",
            "billing_address",
            "being_delivered",
            "coupon",
            "refund_requested"
        )
    
    def create(self, validated_data):
        books_data = validated_data.pop('books')
        order = Order.objects.create(**validated_data)

        for book_data in books_data:
            OrderBook.objects.create(order=order, **book_data)
            
        return order



