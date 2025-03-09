from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Product
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from .forms import ProductCreateForm
from django.contrib.auth.mixins import PermissionRequiredMixin

class ListProducts(ListView):
    """Отображает все продукты в ассортименте"""
    queryset = Product.objects.all()
    template_name = "products/products_list.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
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
            except Product.DoesNotExist:
                continue
        context['cart_items'] = cart_items
        context['cart_total'] = total
        return context

class CreateProductView(CreateView, PermissionRequiredMixin):
    """Создаёт Продукт"""
    model = Product
    form_class = ProductCreateForm
    permission_required = 'products.add_products'
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        product = form.save()
        return super().form_valid(form)

class ProductDetailView(DetailView):
    """Отображает детали продукта"""
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        context['in_cart'] = str(self.object.pk) in cart
        context['quantity_in_cart'] = cart.get(str(self.object.pk), 0)
        return context

class ProductDeleteView(DeleteView, PermissionRequiredMixin):
    """Удаляет продукты"""
    model = Product
    permission_required = 'products.delete_product'
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy('list')

