from django.shortcuts import render
from django.urls import reverse_lazy
from loguru import logger
from .models import Order, OrderItem
from .forms import OrderForm, MenuItemForm, OrderItemForm

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


# 🔹 Обновление заказа
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("order_list")


# 🔹 Удаление заказа
class OrderDeleteView(DeleteView):
    model = Order
    template_name = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("order_list")


def menu_input_view(request):
    menu_items = request.session.get(
        "menu_items", []
    )  # Загружаем список блюд из сессии

    logger.info(menu_items)

    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            # Добавляем блюдо в список
            menu_items.append(
                {
                    "product_name": form.cleaned_data["product_name"],
                    "price": float(form.cleaned_data["price"]),
                }
            )
            request.session["menu_items"] = menu_items  # Сохраняем в сессии

            logger.info(menu_items)

            form = MenuItemForm()  # Очищаем форму после отправки
    else:
        form = MenuItemForm()

    return render(
        request, "orders/menu_input.html", {"form": form, "menu_items": menu_items}
    )


# =================================================================
from django.shortcuts import render, redirect
from .forms import OrderForm, MenuItemForm
from .models import Order, OrderItem


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
