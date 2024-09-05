from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('statistics/', views.statistics, name='statistics'),
    path('ozon/', views.ozon_view, name='ozon'),
    path('wildberries/', views.wildberries, name='wildberries'),
    path('yandex/', views.yandex, name='yandex'),
]