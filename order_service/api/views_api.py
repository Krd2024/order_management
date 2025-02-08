from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import transaction
from rest_framework import status

from order_service.api.serializers import (
    CreateOrderSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from order_service.models import Order, OrderItem


def response(order: object) -> dict[str, int | str, list[dict[str, str | str, int]]]:
    response_data = {
        "Заказ": order.id,
        "Стол": order.table_number,
        "На столе": [
            {"Блюдо": item.product_name, "Цена": float(item.price)}
            for item in order.items.all()
        ],
        "Итого": float(order.total_price),
    }
    return response_data


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для управления заказами."""

    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    serializer_create_class = CreateOrderSerializer

    def get_queryset(self):
        return Order.objects.all()

    @extend_schema(
        request=serializer_create_class,
        examples=[
            OpenApiExample(
                name="Пример заказа",
                value={
                    "table_number": 10,
                    # "status": "pending",
                    "items": [
                        {"product_name": "Суп", "price": 250.0},
                        {"product_name": "Салат", "price": 200.0},
                        {"product_name": "Компот", "price": 100.0},
                    ],
                },
                request_only=True,  # Пример только для тела запроса
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        """Создаёт заказ с блюдами"""
        try:
            # Откат при ошибке
            with transaction.atomic():
                serializer = CreateOrderSerializer(data=request.data)
                if serializer.is_valid():
                    order = serializer.save()

                    # Формирует ответ
                    response_data = response(order)

                    # Возвращает успешный ответ
                    return Response(response_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        description="Обновить заказ (PUT)",
        request=serializer_class,
    )
    def update(self, request, *args, **kwargs):
        return super().update(self, request, *args, **kwargs)

    @extend_schema(
        description="Частичное обновление заказа (PATCH)",
        request=serializer_class,
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Получить конкретный заказ по ID",
        request=serializer_class,
    )
    def retrieve(self, request, pk):
        """Получает один заказ с деталями"""

        order = get_object_or_404(self.get_queryset(), pk=pk)

        response_data = response(order)

        return Response(response_data)

    # serializer_class = OrderItemSerializer

    # return super().retrieve(request, id)

    @extend_schema(description="Получить список всех заказов")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(description="Удалить заказ")
    @extend_schema(request=serializer_class)
    def destroy(request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return Order.objects.all()

    @extend_schema(description="Получить конкретный заказ по ID")
    @extend_schema(request=serializer_class)
    def retrieve(self, request, id: int = None):
        return super().retrieve(request, id)
