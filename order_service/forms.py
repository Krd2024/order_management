from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    """Форма для создания и редактирования заказа.

    - table_number (int): Номер стола, обязательное поле, должно быть больше 0.
    - status (str): Статус заказа с возможными значениями:
        - "pending" (В ожидании)
        - "ready" (Готово)
        - "paid" (Оплачено)
    """

    table_number = forms.IntegerField(
        label="Номер стола",
        min_value=1,
        # required=False,
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
    )
    status = forms.ChoiceField(
        label="Текущий статус",
        choices=[
            ("pending", "В ожидании"),
            ("ready", "Готово"),
            ("paid", "Оплачено"),
        ],
        initial="pending",
        required=False,
        widget=forms.Select(attrs={"class": "form-control form-control-sm"}),
    )

    class Meta:
        model = Order
        fields = ["table_number", "status"]


class OrderItemForm(forms.ModelForm):
    """Форма для добавления позиции (блюда) в заказ.

    - order (Order): Ссылка на заказ, к которому относится блюдо.
    - product_name (str): Название блюда, обязательное поле.
    - price (Decimal): Цена блюда, не может быть отрицательной.
    """

    class Meta:
        model = OrderItem
        fields = ["order", "product_name", "price"]


class MenuItemForm(forms.Form):
    """
    Форма для создания списка (блюдо + цена)

    - product_name (str): Название блюда, обязательное поле.
    - price (Decimal): Цена блюда, не может быть отрицательной.


    """

    product_name = forms.CharField(
        label="Название блюда",
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control form-control-sm"}),
    )
    price = forms.DecimalField(
        label="Цена",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}),
    )
