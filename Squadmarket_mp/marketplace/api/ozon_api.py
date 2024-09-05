import requests
from datetime import datetime, timedelta
from django.conf import settings
from ..models import OzonOrder
from authentication.models import UserSettings
from django.db import transaction

def fetch_ozon_orders(user, date_from, date_to, schema):
    try:
        user_settings = UserSettings.objects.get(user=user)
        api_key = user_settings.ozon_api_key
        client_id = user_settings.ozon_client_id
    except UserSettings.DoesNotExist:
        raise Exception("Настройки пользователя не найдены. Пожалуйста, настройте свои учетные данные API OZON.")

    headers = {
        'Client-Id': str(client_id),
        'Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    all_orders = []
    current_date = date_from
    
    while current_date <= date_to:
        next_date = min(current_date + timedelta(days=1), date_to + timedelta(days=1))
        offset = 0
        
        while True:
            data = {
                "dir": "ASC",
                "filter": {
                    "since": current_date.strftime('%Y-%m-%dT00:00:00.000Z'),
                    "to": next_date.strftime('%Y-%m-%dT00:00:00.000Z')
                },
                "limit": 1000,
                "offset": offset,
                "with": {
                    "analytics_data": True,
                    "financial_data": True
                }
            }

            print(f"Запрос данных за период: {data['filter']['since']} - {data['filter']['to']}, смещение: {offset}")

            url = 'https://api-seller.ozon.ru/v2/posting/fbo/list' if schema == 'FBO' else 'https://api-seller.ozon.ru/v2/posting/fbs/list'
            
            response = requests.post(url, headers=headers, json=data)
            print("URL запроса:", url)
            print("Заголовки запроса:", headers)
            print("Данные запроса:", data)
            print("Код статуса ответа:", response.status_code)
            print("Содержимое ответа:", response.text[:500])  # Печатаем только первые 500 символов ответа
            
            if response.status_code != 200:
                raise Exception(f"Ошибка запроса API с кодом статуса {response.status_code}: {response.text}")

            result = response.json()
            orders = result.get('result', [])

            if not orders:
                break  # Если нет заказов, прерываем внутренний цикл

            all_orders.extend(orders)
            
            if len(orders) < data['limit']:
                break  # Если получено меньше заказов, чем лимит, прерываем внутренний цикл
            
            offset += len(orders)

        current_date = next_date
        if current_date > date_to:
            break  # Прерываем внешний цикл, если текущая дата превысила конечную дату

    created_count = 0
    updated_count = 0

    with transaction.atomic():
        for order_data in all_orders:
            order, created = OzonOrder.objects.update_or_create(
                order_number=order_data['order_number'],
                defaults={
                    'order_id': order_data['order_id'],
                    'posting_number': order_data['posting_number'],
                    'status': order_data['status'],
                    'created_at': datetime.fromisoformat(order_data['created_at'].rstrip('Z')),
                    'in_process_at': datetime.fromisoformat(order_data['in_process_at'].rstrip('Z')) if order_data.get('in_process_at') else None,
                    'cancel_reason_id': order_data.get('cancel_reason_id'),
                    'product_names': ', '.join([product['name'] for product in order_data['products']]),
                    'region': order_data['analytics_data']['region'],
                    'city': order_data['analytics_data']['city'],
                    'warehouse_name': order_data['analytics_data']['warehouse_name'],
                    'product_price': order_data['products'][0]['price'] if order_data['products'] else 0,
                    'product_commission': order_data.get('financial_data', {}).get('products', [{}])[0].get('commission_amount', 0),
                    'delivery_expenses': order_data.get('financial_data', {}).get('products', [{}])[0].get('item_services', {}).get('marketplace_service_item_deliv_to_customer', 0),
                    'schema': schema,
                    'client': user
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

    return f"Обработано заказов: {len(all_orders)}. Создано новых: {created_count}. Обновлено существующих: {updated_count}."