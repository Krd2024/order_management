from django.urls import reverse
import pytest

from order_service.models import Order, OrderItem


@pytest.mark.django_db
def test_create_order(client):
    """
    Тест на создание заказа через представление `create_order_view`.

    1. Добавить тестовые блюда в сессию (имитация выбора блюд пользователем).
    2. Отправить POST-запрос на создание заказа.
    3. Проверить, что:
       - Сервер ответил кодом 200.
       - В базе данных создан один заказ.
       - В заказ добавлены два блюда.
    """

    # Добавить тестовые блюда в сессию пользователя
    session = client.session
    session["menu_items"] = [
        {"product_name": "Тестовая пицца", "price": 1000},
        {"product_name": "Тестовый бургер", "price": 500},
    ]
    session.save()

    # Отправить POST-запрос для оформления заказа
    order_data = {"table_number": 77, "submit_order": "true"}
    response = client.post(reverse("create_order"), order_data, follow=True)

    # 3. Проверяем результаты
    assert response.status_code == 200  # Проверить, что запрос успешен
    assert Order.objects.count() == 1  # Проверить, что в БД создан один заказ
    assert OrderItem.objects.count() == 2  # Проверить, что у заказа два блюда


@pytest.mark.django_db
def test_read_order(client):
    """
    Тест чтения (просмотра) заказа.

    - Создаёт заказ с блюдами.
    - Отправляет GET-запрос на страницу просмотра заказа.
    - Проверяет, что заказ отображается корректно.
    """

    order = Order.objects.create(table_number=10)
    OrderItem.objects.create(order=order, product_name="Тестовая пицца", price=1000)
    OrderItem.objects.create(order=order, product_name="Тестовый бургер", price=500)

    response = client.get(reverse("order_detail", args=[order.id]))

    assert response.status_code == 200
    assert "Тестовая пицца" in response.content.decode()
    assert "Тестовый бургер" in response.content.decode()


@pytest.mark.django_db
def test_update_order(client):
    """
    Тест обновления заказа.

    - Создаёт заказ.
    - Отправляет POST-запрос с обновлёнными данными.
    - Проверяет, что изменения сохранены.
    """

    # Создать заказ со столом №5
    order = Order.objects.create(table_number=5)

    # Создать переменную для обновления обновления стола
    update_data = {"table_number": 77}

    # POST запрос для обновления
    response = client.post(
        reverse("order_update", args=[order.id]), update_data, follow=True
    )

    # Загрузить объект из базы с обновленными данными
    order.refresh_from_db()

    assert response.status_code == 200
    assert order.table_number == 77  # Проверить, что номер стола изменился


@pytest.mark.django_db
def test_delete_order(client):
    """
    Тест удаления заказа.

    - Создаёт заказ.
    - Отправляет POST-запрос на удаление.
    - Проверяет, что заказ удалён.
    """
    # Зоздать заказ
    order = Order.objects.create(table_number=99)

    # POST запрос на удаление заказа
    response = client.post(reverse("order_delete", args=[order.id]), follow=True)

    assert response.status_code == 200
    assert Order.objects.count() == 0  # Проверить, что заказ удалён
