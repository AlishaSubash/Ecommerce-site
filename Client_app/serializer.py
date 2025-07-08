from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class User_detailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_details
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = task
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = book
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = publisher
        fields = '__all__'


class AdminOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = admin_order
        fields = '__all__'

class AdminOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = admin_order_item
        fields = '__all__'