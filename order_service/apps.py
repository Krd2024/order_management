from django.apps import AppConfig


class OrderServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order_service"

    def ready(self):
        """Подключает сигнал обновления общей суммы
        при добавлении или удалении блюда
        """
        import order_service.service.signal.total_price  # noqa
