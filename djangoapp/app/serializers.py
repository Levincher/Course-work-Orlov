from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'created_at', 'updated_at', 'user_info']

    # noinspection PyMethodMayBeStatic
    def get_user_info(self, obj):
        user = obj.user
        user_serializer = UserSerializer(user)
        return user_serializer.data


class ExecutorSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Executor
        fields = ['id', 'user', 'created_at', 'updated_at', 'user_info']

    # noinspection PyMethodMayBeStatic
    def get_user_info(self, obj):
        user = obj.user
        user_serializer = UserSerializer(user)
        return user_serializer.data


class OrderSerializer(serializers.ModelSerializer):
    cust_id = CustomerSerializer()
    exec_id = ExecutorSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    # noinspection PyMethodMayBeStatic
    def get_price(self, obj: Payment):
        return obj.order.price


class DiscussSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    message_sender = serializers.PrimaryKeyRelatedField(source='order_id.cust_id', read_only=True)
    message_receiver = serializers.PrimaryKeyRelatedField(source='order_id.exec_id', read_only=True)

    class Meta:
        model = Discuss
        exclude = ['timestamp']


class FeedbackSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = Feedback
        fields = '__all__'
