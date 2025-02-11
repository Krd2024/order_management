from django.urls import path
from .views import (
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    OrderUpdateView,
    create_order_view,
    delete_dich,
    list_sorted,
    main,
    search_order_list,
    add_dich,
    get_revenue,
)

urlpatterns = [
    path("", main, name="main"),
    path("list/", OrderListView.as_view(), name="order_list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    path("create-order/", create_order_view, name="create_order"),
    path("search-order/", search_order_list, name="search_order_list"),
    path("<int:pk>/dich-delete/", delete_dich, name="dish_delete"),
    path("<int:pk>/dich-add/", add_dich, name="add_dich"),
    path("revenue/", get_revenue, name="how_many_are_there"),
    path("list/sorted/<str:choice>", list_sorted, name="list_sorted"),
]
