from rest_framework.serializers import ModelSerializer

from .models import Order, OrderProduct



class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class ApplicationSerializer(ModelSerializer):
    products = ParticipantSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname', 'address', 'phonenumber']
