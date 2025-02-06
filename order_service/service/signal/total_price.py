from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from order_service.models import OrderItem


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """Обновить сумму заказа при изменении товаров"""
    instance.order.update_total_price()
