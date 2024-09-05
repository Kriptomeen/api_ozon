from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .api.ozon_api import fetch_ozon_orders
from datetime import datetime, timedelta
from django.contrib import messages
from .models import OzonOrder
from django.db.models import Q

def home(request):
    return render(request, 'marketplace/home.html')

@login_required
def statistics(request):
    return render(request, 'marketplace/statistics.html')

@login_required
def ozon_view(request):
    if request.method == 'POST':
        date_from = datetime.strptime(request.POST['date_from'], '%Y-%m-%d')
        date_to = datetime.strptime(request.POST['date_to'], '%Y-%m-%d')
        schema = request.POST.get('schema')

        if schema not in ['FBO', 'FBS']:
            messages.error(request, 'Пожалуйста, выберите схему продаж (FBO или FBS).')
            return render(request, 'marketplace/ozon.html')

        # Проверяем, не превышает ли выбранный период 30 дней
        max_period = timedelta(days=30)
        if date_to - date_from > max_period:
            messages.error(request, 'Выбранный период превышает 30 дней. Пожалуйста, выберите период не более 30 дней.')
            return render(request, 'marketplace/ozon.html', {'date_from': date_from.strftime('%Y-%m-%d'), 'date_to': date_to.strftime('%Y-%m-%d'), 'schema': schema})

        try:
            result = fetch_ozon_orders(request.user, date_from, date_to, schema)
            messages.success(request, f'Успешно обработаны заказы по схеме {schema} за период с {date_from.date()} по {date_to.date()}. {result}')
        except Exception as e:
            messages.error(request, f'Произошла ошибка при загрузке заказов: {str(e)}')
    
    # Получаем параметры для таблицы из GET-запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    columns = request.GET.getlist('columns')

    # Если даты не указаны, используем последние 5 дней
    if not start_date or not end_date:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=5)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Получаем заказы FBO за указанный период
    orders = OzonOrder.objects.filter(
        Q(created_at__date__gte=start_date) & 
        Q(created_at__date__lte=end_date) & 
        Q(schema='FBO') &
        Q(client=request.user)
    ).order_by('-created_at')

    # Получаем все доступные столбцы из модели OzonOrder
    available_columns = [field.name for field in OzonOrder._meta.get_fields() if field.name != 'client']

    # Если столбцы не указаны, используем все доступные
    if not columns:
        columns = available_columns

    context = {
        'orders': orders,
        'columns': columns,
        'available_columns': available_columns,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'marketplace/ozon.html', context)

@login_required
def wildberries(request):
    return render(request, 'marketplace/wildberries.html')

@login_required
def yandex(request):
    return render(request, 'marketplace/yandex.html')