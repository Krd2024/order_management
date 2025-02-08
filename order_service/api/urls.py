from rest_framework.routers import DefaultRouter
from django.urls import include, path

from order_service.api.views_api import OrderViewSet


router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("v1/", include(router.urls)),
]
