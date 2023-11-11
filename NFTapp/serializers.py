from rest_framework import serializers
from .models import TradeHistory, User, NFTProduct

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')  # Add other fields as needed

class NFTProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTProduct
        fields = ('id', 'name', 'description')  # Add other fields as needed

class TradeHistorySerializer(serializers.ModelSerializer):
    buyer = UserSerializer()
    seller = UserSerializer()
    product = NFTProductSerializer()

    class Meta:
        model = TradeHistory
        fields = ('id', 'buyer', 'seller', 'product', 'price_at_purchase', 'quantity_at_purchase', 'timestamp')
        read_only_fields = ('id', 'timestamp')