from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from products.models import Product
from django.http import HttpResponseBadRequest


class AddToCart(View):
    """Добавляет продукт в корзину"""
    def post(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        cart = request.session.get('cart', {})
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity) if quantity else 1
            if quantity > 0:
                cart[str(product_pk)] = cart.get(str(product_pk), 0) + quantity
            elif quantity == 0:
                pass
            else:
                return HttpResponseBadRequest("Количество не может быть отрицательным")
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Неверное значение количества")
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart_view')

    def get(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        cart = request.session.get('cart', {})
        cart[str(product_pk)] = cart.get(str(product_pk), 0) + 1
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart_view')

class UpdateCartView(View):
    """Обновляет количество продукта в корзине"""
    def post(self, request, product_pk):
        cart = request.session.get('cart', {})
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity) if quantity else 0
            if quantity > 0:
                cart[str(product_pk)] = quantity
            else:
                cart.pop(str(product_pk), None)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Неверное значение количества")
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart_view')

    def get(self, request, product_pk):
        cart = request.session.get('cart', {})
        quantity = request.GET.get('quantity')
        try:
            quantity = int(quantity) if quantity else 0
            if quantity == 0:
                cart.pop(str(product_pk), None)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Неверное значение количества")
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart_view')

class CartView(TemplateView):
    """Отображает корзину"""
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        cart_items = []
        total = 0
        for product_pk, quantity in cart.items():
            try:
                product = Product.objects.get(pk=product_pk)
                subtotal = product.price * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                total += subtotal
            except Product.DoesNotExists:
                continue
        context['cart_items'] = cart_items
        context['total'] = total
        return context
