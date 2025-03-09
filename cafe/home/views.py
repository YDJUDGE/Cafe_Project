from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    """Домашняя страница сайта"""
    template_name = "main_page/home.html"

# Обработка ошибка
def custom_404(request, exception):
    """Кастомная обработка ошибки 404"""
    return render(request, 'errors/404.html', status=404)
