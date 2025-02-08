from rest_framework import serializers
from order_service.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):

    table_number = serializers.IntegerField(min_value=1)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0.00
    )
    # Вывод по-русски
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "table_number", "total_price", "status"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
