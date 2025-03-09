from django.urls import path
from .views import ListProducts, CreateProductView, ProductDetailView, ProductDeleteView

urlpatterns = [
    path("", ListProducts.as_view(), name="list"),
    path("create/", CreateProductView.as_view(), name="create_product"),
    path("<int:pk>/confirm_delete/", ProductDeleteView.as_view(), name="delete_product"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail_product"),
]
