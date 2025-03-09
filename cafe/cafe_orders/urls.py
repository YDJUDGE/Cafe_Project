from django.urls import path
from .views import OrderListView, OrderCreateView, OrderDetailView, ChangeOrderStatusView, DeleteOrderView

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("<int:pk>/", OrderDetailView.as_view(), name='order_detail'),
    path("change-status/", ChangeOrderStatusView.as_view(), name='change_status'),
    path("delete-order/", DeleteOrderView.as_view(), name='delete_order')
]
