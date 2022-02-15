from rest_framework.serializers import ModelSerializer

from .models import Order, OrderProduct



class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'fixed_price']


class OrderSerializer(ModelSerializer):
    products = OrderProductSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname', 'address', 'phonenumber']
