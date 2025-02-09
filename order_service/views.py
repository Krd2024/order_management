from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import OrderForm, MenuItemForm
from .models import Order, OrderItem
from loguru import logger

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    # CreateView,
    UpdateView,
    DeleteView,
)


def main(request):
    """Главная страница"""
    return render(request, "main.html")


class OrderListView(ListView):
    """Список заказов"""

    model = Order
    template_name = "orders/orders_list.html"
    context_object_name = "orders"


class OrderDetailView(DetailView):
    """Детали заказа"""

    model = Order
    template_name = "orders/order_detail.html"


# class OrderCreateView(CreateView):
#     """Создание заказа"""

#     model = Order
#     form_class = OrderForm
#     template_name = "orders/order_form.html"
#     success_url = reverse_lazy("order_list")


class OrderUpdateView(UpdateView):
    """Обновление заказа"""

    model = Order
    form_class = OrderForm
    # menu_item_form = MenuItemForm
    # template_name = "orders/create_order.html"
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("order_list")


class OrderDeleteView(DeleteView):
    """Удаление заказа"""

    model = Order
    # Прейти на страницу подтверждения удаления
    template_name = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("order_list")


def search_order_list(request):
    """
    Функция для поиска заказов по разным параметрам.

    Первым проверяеся запросна изменение статуса
    Если не статус, значит запрос должен бать числом для ID заказа
    или номера стола.
    """

    # Полуает введенное значение
    choice_search = request.GET.get("choice_search")

    orders = Order.objects.all()

    # Поиск по статусу
    if choice_search == "status":
        print(status := request.GET.get("status"))
        orders = orders.filter(status=status)
        return render(request, "orders/orders_list.html", {"orders": orders})

    # Получает введенную строку поиска и удаляет пробелы
    search_query = request.GET.get("search", "").strip()

    # Если строка поиска не является числом, выводим ошибку
    if not search_query.isdigit():
        messages.error(request, "Ошибка! Проверьте введенные данные.")
        return redirect("order_list")

    # Поиск по номеру заказа
    if choice_search == "order_id":
        orders = orders.filter(id=search_query)

    # Поиск по номеру стола
    elif choice_search == "table_number":
        orders = orders.filter(table_number=search_query)
    return render(request, "orders/orders_list.html", {"orders": orders})


def create_order_view(request):
    """Создание заказа и добавление блюд в заказ.
    Создвёт список из блюд и цены перед созданием заказа
    """
    # Список блюд из сессии
    menu_items = request.session.get("menu_items", [])
    if request.method == "POST":
        # Если форма для блюда была отправлена
        if "add_item" in request.POST:
            # Инициализация форм для добавления блюда и оформления заказа
            # с переданными данными из POST-запроса
            menu_item_form = MenuItemForm(request.POST)
            order_form = OrderForm(request.POST)

            if menu_item_form.is_valid():
                # Добавляем блюдо в список
                menu_items.append(
                    {
                        "product_name": menu_item_form.cleaned_data["product_name"],
                        "price": float(menu_item_form.cleaned_data["price"]),
                    }
                )
                # Сохраняем в сессии
                request.session["menu_items"] = menu_items

                logger.info(request.session)
                # Очищаем форму после отправки
                menu_item_form = MenuItemForm()
        # Если форма для заказа была отправлена
        elif "submit_order" in request.POST:
            # Проверяет, есть ли в заказе блюда
            if request.session["menu_items"] == []:
                # Сообщение на страницу
                messages.success(request, "Заказан столик без блюд.")
                messages.error(request, "Cо своими напитками и едой нельзя!")

            # Создать объект формы с данными из запроса
            order_form = OrderForm(request.POST)
            # Проверить данные на валидность
            if order_form.is_valid():
                # Сохранить заказ
                order = order_form.save()
                try:
                    # Сохраняем все блюда для этого заказа
                    for item in menu_items:
                        OrderItem.objects.create(
                            order=order,
                            product_name=item["product_name"],
                            price=item["price"],
                        )
                    # Очистить список блюд
                    request.session["menu_items"] = []
                    messages.success(request, "Заказ успешно создан!")
                    return redirect("order_list")
                except Exception as e:
                    logger.error(f"❗Ошибка {e}")
                    messages.error(request, "Ошибка при создании заказа.")
            else:
                messages.error(request, "Ошибка! Проверьте введенные данные.")

    else:
        order_form = OrderForm()
        menu_item_form = MenuItemForm()
    return render(
        request,
        "orders/create_order.html",
        {
            "order_form": order_form,
            "menu_item_form": menu_item_form,
            "menu_items": menu_items,
        },
    )


def delete_dich(request, pk: int) -> None:
    """
    Удаляет блюдо из заказа и перенаправляет
    обратно в детали заказа.
    """
    try:
        # Получить объект
        dish = get_object_or_404(OrderItem, pk=pk)
        # Удал объект
        dish.delete()
        # Успешное сообщение
        messages.success(request, "Блюдо успешно удалено из заказа.")
    except Exception as e:
        # Ошибки, которые могут возникнуть
        messages.error(request, f"Произошла ошибка при удалении блюда: {str(e)}")
    # Перенаправить на страницу с деталями заказа
    return redirect("order_detail", pk=dish.order.pk)


def add_dich(request, pk: int):
    """
    Добавляет блюдо в заказ и перенаправляет
    обратно в детали заказа.
    """
    if request.method == "POST":
        product_name = request.POST.get("product_name")
        price = request.POST.get("price")

        if product_name and price:
            try:
                # Получить объект
                order = get_object_or_404(Order, id=pk)
                # Обновить заказ (добавить блюдо)
                OrderItem.objects.create(
                    order=order, product_name=product_name, price=price
                )
                messages.success(request, f"{product_name} добавлен(а)!")
            except Exception as e:
                # Ошибки, которые могут возникнуть
                messages.error(request, f"Произошла ошибка: {str(e)}")
    # Перенаправить на страницу с деталями заказа
    return redirect("order_detail", pk)


def get_revenue(request):
    """Считает выручку заказов со статусом 'Оплачено'"""

    # Получить объекты со статусом 'Оплачено'
    sum_many = Order.objects.filter(status="paid")
    # Получить сумму итератора из сумм каждого заказа
    revenue = sum(_.total_price for _ in sum_many)
    print(revenue)

    return render(request, "orders/order_revenue.html", {"revenue": revenue})
