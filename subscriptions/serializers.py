from rest_framework import serializers
from .models import Customer, Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerDataSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    id = serializers.IntegerField()
    subscriptions = SubscriptionSerializer(many=True)
    accumulated_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        fields = ('customer_name', 'id', 'subscriptions', 'accumulated_price')

class SubscriptionPriceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    subscriptions = SubscriptionSerializer(many=True)
    accumulated_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Subscription
        fields = ['customer', 'subscriptions', 'accumulated_price']
