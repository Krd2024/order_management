from django.urls import path
from .views import (
    # OrderCreateView,
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    OrderUpdateView,
    create_order_view,
    delete_dich,
    main,
    search_order_list,
    add_dich,
    get_revenue,
)

urlpatterns = [
    path("", main, name="main"),
    path("list/", OrderListView.as_view(), name="order_list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    # path("create/", OrderCreateView.as_view(), name="order_create"),
    path("<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("create-order/", create_order_view, name="create_order"),
    path("filter-order/", search_order_list, name="search_order_list"),
    path("dish-delete/<int:pk>/", delete_dich, name="dish_delete"),
    path("dich-add/<int:pk>/", add_dich, name="add_dich"),
    path("revenue/", get_revenue, name="how_many_are_there"),
]
