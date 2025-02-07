from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Order(models.Model):
    table_number = models.IntegerField(verbose_name="Номер стола")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "В ожидании"),
            ("ready", "Готов"),
            ("paid", "Оплачено"),
        ],
        default="pending",
    )

    # def clean_product_name(self):
    #     table_number = self.cleaned_data.get("table_number", "")
    #     if not table_number:  # Если пустое, заменяем на дефолтное значение
    #         return "Не указано"
    #     return table_number

    @property
    def items(self):
        """Возвращает список заказов"""
        return self.order_items.all()

    def update_total_price(self):
        """Обновляет общую стоимость. Срабатывает от сигнала
        при добавлениии или удалении из таблицы блюда.

        """
        self.total_price = sum(item.price for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Заказ {self.id} - Стол {self.table_number} - {self.items} - {self.total_price} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
