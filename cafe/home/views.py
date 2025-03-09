from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    """Домашняя страница сайта"""
    template_name = "main_page/home.html"

# Обработка ошибка
def custom_404(request, exception):
    """Кастомная обработка ошибки 404"""
    return render(request, 'errors/404.html', status=404)
def custom_403(request, exception):
    """Кастомная обработка ошибки 403"""
    return render(request, 'errors/403.html', status=403)
