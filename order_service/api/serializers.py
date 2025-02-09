from decimal import Decimal
from jsonschema import ValidationError
from rest_framework import serializers
from order_service.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["product_name", "price"]


class OrderSerializer(serializers.ModelSerializer):

    table_number = serializers.IntegerField(min_value=1)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    # Вывод по-русски
    status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "table_number", "total_price", "status"]


class CreateOrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказа."""

    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ["table_number", "items"]

    def validate(self, data):
        """Проверяет является ли число положительным"""

        items = data.get("items", [])
        for item in items:
            if item["price"] < 0:
                raise serializers.ValidationError("Цена не может быть отрицательной.")
        return data

    def create(self, validated_data):
        """Создание заказа и его позиций."""

        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
