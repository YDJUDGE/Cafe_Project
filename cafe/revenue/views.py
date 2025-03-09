from django.shortcuts import render
from django.views import View
from django.utils import timezone
from cafe_orders.models import Order
from datetime import datetime, timedelta


class RevenueView(View):
    template_name = 'revenue/revenue.html'

    def get(self, request, *args, **kwargs):
        paid_orders = Order.objects.filter(status='paid')

        total_revenue = sum(float(order.total_price) if order.total_price else 0 for order in paid_orders)
        paid_orders_count = paid_orders.count()

        context = {
            'total_revenue': total_revenue,
            'paid_orders_count': paid_orders_count,
        }

        return render(request, self.template_name, context)
