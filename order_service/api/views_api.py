from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from order_service.api.serializers import OrderSerializer, OrderItemSerializer
from order_service.models import Order, OrderItem


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для управления заказами."""

    # queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.all()

    serializer_class = OrderSerializer

    @extend_schema(description="Создать заказ")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(description="Обновить заказ (PUT)")
    @extend_schema(request=serializer_class)
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
        response = {
            "Заказ": order.id,
            "Стол": order.table_number,
            "На столе": [
                {"Блюдо": item.product_name, "Цена": float(item.price)}
                for item in order.items.all()
            ],
            "Итого": float(order.total_price),
        }

        return Response(response)

    # serializer_class = OrderItemSerializer

    # return super().retrieve(request, id)

    @extend_schema(description="Получить список всех заказов")
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)  # Сериализация списка
        return Response(serializer.data)

        return super().list(request, *args, **kwargs)

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
