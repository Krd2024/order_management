from drf_spectacular.utils import extend_schema, OpenApiExample
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from django.db import transaction
from rest_framework import status

from order_service.api.serializers import (
    OrderSerializer,
    # OrderSerializer,
)
from order_service.models import Order


class CastomSerializer:
    def __init__(
        self, order: object
    ) -> dict[str, int | str, list[dict[str, str | int]]]:

        self.order = order

    def object_to_dict(self):
        response_data = {
            "Заказ": self.order.id,
            "Стол": self.order.table_number,
            "На столе": [
                {"Блюдо": item.product_name, "Цена": float(item.price)}
                for item in self.order.items.all()
            ],
            "Итого": float(self.order.total_price),
        }
        return response_data


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для управления заказами.

    Позволяет:
    - Получать список всех заказов.
    - Получать детали конкретного заказа.
    - Создавать новый заказ.
    - Обновлять существующий заказ.
    - Удалять заказ.
    """

    # Сериализатор для данных заказа
    serializer_class = OrderSerializer

    def get_queryset(self):
        """Запрос для получения всех заказов"""
        return Order.objects.all()

    @extend_schema(
        summary="Создать заказ",
        description="Этот метод создает новый заказ. Необходимо указать номер стола, блюда и цену",
        request=serializer_class,
        examples=[
            OpenApiExample(
                name="Пример заказа",
                value={
                    "table_number": 10,
                    "items": [
                        {"product_name": "Суп", "price": 250.0},
                        {"product_name": "Салат", "price": 200.0},
                        {"product_name": "Компот", "price": 100.0},
                    ],
                },
                # Пример только для тела запроса
                request_only=True,
            )
        ],
    )
    def create(self, request):
        """Создаёт заказ с блюдами.

        - Валидирует входные данные через сериализатор.
        - Создаёт заказ в БД.
        - Возвращает успешный ответ или ошибку.
        """
        try:
            # Откат изменений при ошибке
            with transaction.atomic():
                serializer = OrderSerializer(data=request.data)
                if serializer.is_valid():
                    order: Order = serializer.save()

                    # Формирует ответ
                    response_obj = CastomSerializer(order)
                    response_data = response_obj.object_to_dict()

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
        summary="Обновить заказ",
        description="Возможность полностью обновить заказ.",
        request=serializer_class,
        examples=[
            OpenApiExample(
                name="Пример заказа",
                value={
                    # "id": 1,
                    "table_number": 10,
                    "status": "pending",
                    "items": [
                        {"product_name": "Суп", "price": 250.0},
                        {"product_name": "Салат", "price": 200.0},
                        {"product_name": "Компот", "price": 100.0},
                    ],
                },
                # Пример только для тела запроса
                request_only=True,
            )
        ],
    )
    def update(self, request, pk: int):
        """Обновляет заказ с блюдами.

        - Валидирует входные данные через сериализатор.
        - Обновляет заказ в БД.
        - Возвращает обновленные данные или ошибку.
        """

        # Получаем заказ по pk
        order = get_object_or_404(Order, pk=pk)

        try:
            # Откат при ошибке
            with transaction.atomic():
                # Создаёт сериализатор для обновления
                serializer = self.get_serializer(order, data=request.data)
                # serializer = self.get_serializer(order, data=request.data, partial=True)

                # Проверяет данные на валидность
                if serializer.is_valid():
                    # Сохраняем обновленный заказ
                    updated_order = serializer.save()

                    # Формирует ответ
                    response_obj = CastomSerializer(updated_order)
                    # Вызвать метод преобразования объекта в словарь
                    response_data = response_obj.object_to_dict()

                    # Возврнуть успешный ответ
                    return Response(response_data, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Ошибка 500
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        pass

    @extend_schema(
        summary="Получить заказ",
        description="Получить конкретный заказ по ID",
        # request=serializer_class,
    )
    def retrieve(self, request, pk: int) -> Response:
        """Получает один заказ с деталями.

        - Ищет заказ по переданному 'pk'.
        - Если заказ найден, возвращает его данные.
        - Если заказ не найден, вызывает исключение `Http404`.
        """

        # Получает заказ по первичному ключу (pk), если он не найден, генерируется ошибка 404
        order: Order = get_object_or_404(self.get_queryset(), pk=pk)

        # Формирует ответные данные
        # response_data: dict[str, Any] = response(order)
        response_obj = CastomSerializer(order)
        response_data = response_obj.object_to_dict()

        return Response(response_data)

    @extend_schema(
        summary="Получить заказы",
        description="Получить список всех заказов",
    )
    def list(self, request, *args, **kwargs):
        """Получить список всех заказов.

        - Возвращает список всех заказов, сериализованный через `OrderSerializer`.
        """
        # Получает queryset заказов
        queryset = self.get_queryset()
        # Сериализует данные (множество заказов)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Удалить заказ",
        description="Удалить заказ по ID",
    )
    def destroy(self, request, *args, **kwargs):
        # Получаить объект, который хотим удалить
        instance = self.get_object()
        # Удалить
        self.perform_destroy(instance)
        # Оповестить
        return Response({"message": "Объект успешно удалён"}, status=status.HTTP_200_OK)
