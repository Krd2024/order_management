from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import OrderForm, MenuItemForm
from .models import Order, OrderItem
from loguru import logger

# from .forms import OrderForm, MenuItemForm, OrderItemForm

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


def main(request):
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


# 🔹 Создание заказа
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("order_list")


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
    template_name = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("order_list")


def search_order_list(request):
    search_query = request.GET.get("search", "").strip()  # Получаем введенное значение
    choice_search = request.GET.get("choice_search", "order_id")

    orders = Order.objects.all()

    if search_query.isdigit():  # Проверяет, что введены только цифры
        if choice_search == "order_id":  # Поиск по номеру заказа
            orders = orders.filter(id=search_query)
        elif choice_search == "table_number":  # Поиск по номеру стола
            orders = orders.filter(table_number=search_query)
    elif choice_search == "status":  # Поиск по статусу
        print("--status---")
        orders = orders.filter(status="ready")

    return render(request, "orders/orders_list.html", {"orders": orders})


def create_order_view(request):
    # menu_items = []  # Список блюд для текущего заказа
    menu_items = request.session.get("menu_items", [])  # Список блюд из сессии
    print("--------1--------------")
    if request.method == "POST":
        # Если форма для блюда была отправлена
        print("-----2----")
        print(request.POST.get)
        if "add_item" in request.POST:
            print("-----3----")
            menu_item_form = MenuItemForm(request.POST)
            order_form = OrderForm(request.POST)

            if menu_item_form.is_valid():
                # Добавляем блюдо в список
                print("-----4----")
                menu_items.append(
                    {
                        "product_name": menu_item_form.cleaned_data["product_name"],
                        "price": float(menu_item_form.cleaned_data["price"]),
                    }
                )
                request.session["menu_items"] = menu_items  # Сохраняем в сессии
                logger.info(menu_items)

                menu_item_form = MenuItemForm()  # Очищаем форму после отправки
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

        # Если форма для заказа была отправлена
        elif "submit_order" in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = order_form.save()  # Сохраняем заказ
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
                    return redirect("order_list")
                except Exception as e:
                    logger.error(f"❗Ошибка {e}")
            else:
                order_form = OrderForm(request.POST)
                menu_item_form = MenuItemForm()
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
