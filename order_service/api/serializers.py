from rest_framework import serializers
from order_service.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["product_name", "price"]


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказа."""

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "table_number", "items"]

    def validate(self, data):
        """Проверяет является ли число положительным"""

        items = data.get("items", [])
        for item in items:
            if item["price"] < 0:
                raise serializers.ValidationError("Цена не может быть отрицательной.")
        return data

    def create(self, validated_data):
        """Создание заказа и его позиций."""

        # Извлекает список блюд из запроса
        items_data = validated_data.pop("items")

        # Создать заказ
        order = Order.objects.create(**validated_data)

        # Добавить блюда в заказ
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        """Обновление существующего заказа и его позиций.
        Удаляются все блюда из заказа и записываюся новые
        """

        # Обновляет поле заказа (номер стола)
        instance.table_number = validated_data.get(
            "table_number", instance.table_number
        )
        instance.save()

        # Получает блюда
        items_data = validated_data.get("items", [])

        # Удалить список блюд перед обновлением
        OrderItem.objects.filter(order=instance).delete()
        # Обновить закз новыми блюдами
        for item_data in items_data:
            OrderItem.objects.create(order=instance, **item_data)

        return instance
