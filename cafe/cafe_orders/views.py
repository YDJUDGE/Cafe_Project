from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from .models import Order
from products.models import Product
from django.http import HttpResponseBadRequest, Http404
from .forms import OrderCreateForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

class OrderCreateView(CreateView):
    """Создаёт новый заказ на основе корзины"""
    model = Order
    form_class = OrderCreateForm
    template_name = "orders/order_create.html"
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        cart = self.request.session.get('cart', {})
        if not cart:
            return redirect('cart_view')

        items = []
        total_price = 0
        for product_pk, quantity in cart.items():
            try:
                product = Product.objects.get(pk=product_pk)
                item = {
                    'product_pk': product.pk,
                    'name': product.name,
                    'price': float(product.price),
                    'quantity': quantity
                }
                items.append(item)
                total_price += product.price * quantity
            except Product.DoesNotExist:
                return "Продукт не найден"

        order = form.save(commit=False)
        order.items = items
        order.total_price = total_price
        order.save()
        del self.request.session['cart']
        self.request.session.modified = True
        return super().form_valid(form)

class OrderDetailView(DetailView):
    """Отображает детали заказа"""
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items_with_totals = [{
            "name": item.get('name', "Нет"),
            "quantity": item.get('quantity', 1),
            "price": item.get('price', 0),
            "total": item.get('price', 0) * item.get('quantity', 1)
        }
            for item in self.object.items or []
        ]
        context['items_with_totals'] = items_with_totals
        context['status_choices'] = Order._meta.get_field('status').choices
        return context

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        status = request.POST.get('status')
        if status in dict(order._meta.get_field('status').choices):
            order.status = status
            order.save()
        else:
            return HttpResponseBadRequest("Недопустимое значение статуса")
        return redirect('order_detail', pk=order.pk)

class OrderListView(ListView):
    """Отображает список всех заказов"""
    model = Order
    template_name = 'orders/orders_list.html'
    context_object_name = 'orders'

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        status = request.POST.get('status')
        if status in dict(order._meta.get_field('status').choices):
            order.status = status
            order.save()
        else:
            return HttpResponseBadRequest("Недопустимое значение статуса")
        return redirect('order_detail', pk=order.pk)

    def get_queryset(self):
        queryset = super().get_queryset()

        """Реализуем параметры поиска"""
        table_number = self.request.GET.get('table_number', '')
        status = self.request.GET.get('status', '')

        if table_number:
            queryset = queryset.filter(table_number=table_number)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """Берем текущие значения поиска в контекст(для отображения формы)"""
        context['table_number'] = self.request.GET.get('table_number', '')
        context['status'] = self.request.GET.get('status', '')
        context['status_choices'] = Order._meta.get_field('status').choices

        """Проверяем, корректен ли номер стола и есть ли заказ на стакой стол"""
        table_number = self.request.GET.get('table_number', '')
        if table_number and table_number.isdigit() and not self.get_queryset().exists():
            context['no_table_message'] = "Такого стола нет"

        return context

class ChangeOrderStatusView(View):
    """Позволяет изменить статус заказа по его ID"""
    template_name = "orders/change_status.html"

    def get(self, request, *args, **kwargs):
        """Передаём список возможных статусов"""
        status_choices = Order._meta.get_field('status').choices
        return render(request, self.template_name, {'status_choices': status_choices})

    def post(self, request, *args, **kwargs):
        """Получаем ID заказа и новый статус"""
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        if not order_id or not new_status:
            messages.error(request, "Пожалуйста, заполните все поля")
            return redirect('change_status')

        try:
            order_id = int(order_id)
        except ValueError:
            messages.error(request, "Пожалуйста введите корректный ID заказа")
            return redirect('change_status')

        order = get_object_or_404(Order, pk=order_id)

        valid_statuses = dict(Order._meta.get_field('status').choices).keys()
        if new_status not in valid_statuses:
            messages.error(request, "Недопустимый статус.")
            return redirect('change_status')

        order.status = new_status
        order.save()
        messages.success(request, f"Статус заказа №{order.pk} успешно обновлён на {order.get_status_display()}")

        return redirect('order_list')

class DeleteOrderView(View):
    """Позволяет удалить заказа по ID"""
    template_name = 'orders/delete_order.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')

        if not order_id:
            messages.error(request, "Пожалуйста, введите ID заказа")
            return redirect('delete_order')

        try:
            order_id = int(order_id)
            order = Order.objects.get(pk=order_id)
        except ValueError:
            messages.error(request, "ID заказа должен быть числом")
            return redirect('delete_order')
        except ObjectDoesNotExist:
            raise Http404("Заказ не нйаден")

        order.delete()
        messages.success(request, "Заказ успешно удалён")

        return redirect('order_list')

