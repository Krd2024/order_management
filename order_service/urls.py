from django.urls import path
from .views import (
    # OrderCreateView,
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    OrderUpdateView,
    create_order_view,
    dish_delete,
    main,
    search_order_list,
    # menu_input_view,
)

urlpatterns = [
    path("", main, name="main"),
    path("list/", OrderListView.as_view(), name="order_list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    # path("create/", OrderCreateView.as_view(), name="order_create"),
    path("<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    # path("menu-input/", menu_input_view, name="menu_input"),
    path("create-order/", create_order_view, name="create_order"),
    path("filter-order/", search_order_list, name="search_order_list"),
    path("dish-delete/<int:pk>/", dish_delete, name="dish_delete"),
]
