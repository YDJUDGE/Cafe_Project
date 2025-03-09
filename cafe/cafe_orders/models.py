from django.db import models
from django.db.models import Manager
from django.utils import timezone
from typing import TYPE_CHECKING

class Order(models.Model):
    """Модель заказа"""
    table_number = models.PositiveIntegerField(verbose_name="Номер стола")
    items = models.JSONField(verbose_name="Список заказанных блюд", default=list)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость", default=0.00)
    status = models.CharField(max_length=20, choices=[
        ("pending", "В ожидании"),
        ("ready", "Готово"),
        ("paid", "Оплачено")
    ],

    default="pending",
    verbose_name="Статус заказа"

        )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    if TYPE_CHECKING:
        objects: Manager

    def __str__(self):
        return f"Заказ # {self.pk} - Стол {self.table_number}"

    def save(self, *args, **kwargs):
        """Вычисляем итоговую цену перед сохранением"""
        if self.items:
            self.total_price = sum(item.get('price', 0) * item.get('quantity', 1) for item in self.items)
        super().save(*args, **kwargs)

    def get_item_total(self, item):
        """Вычисляет общую стоимость"""
        return item.get('price', 0) * item.get('quantity', 1)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
