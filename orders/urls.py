from django.urls import path

from orders.apps import OrdersConfig
from orders.views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView, RevenueView

app_name = OrdersConfig.name

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("update/<int:pk>/", OrderUpdateView.as_view(), name="order_update"),
    path("delete/<int:pk>/", OrderDeleteView.as_view(), name="order_delete"),
    path("revenue/", RevenueView.as_view(), name="revenue_view"),
]
