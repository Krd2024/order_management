from django.apps import AppConfig


class OrderServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order_service"

    def ready(self):
        import order_service.service.signal.total_price  # noqa
