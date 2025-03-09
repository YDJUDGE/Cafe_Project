from django.urls import path
from .views import RevenueView

urlpatterns = [
    path('', RevenueView.as_view(), name='revenue')
]
