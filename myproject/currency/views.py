from django.http import JsonResponse
from .models import CurrencyRequest
import requests
from datetime import datetime, timedelta

last_request_time = None

def get_current_usd(request):
    """
    Получает и возвращает текущий курс обмена доллара США к рублю в формате JSON.
    Выполняет запрос к внешнему API для получения курса, если с момента последнего запроса прошло более 10 секунд.
    Возвращает данные о текущем курсе и информацию о последних 10 запросах.

    Args:
        request (HttpRequest): Объект HttpRequest, который содержит метаданные о запросе.

    Returns:
        JsonResponse: Объект JsonResponse, содержащий текущий курс и историю запросов.
    """
    
    global last_request_time
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest', }

    url = 'https://cbr.ru/Queries/AjaxDataSource/112805'

    data_dollar = {
        'DT': '',
        'val_id': 'R01235',
        '_': '1705996737045'
    }
    
    now = datetime.now()

    # Проверка, был ли запрос более 10 секунд назад
    if last_request_time is None or now - last_request_time > timedelta(seconds=10):
        
        response = requests.get(url=url, headers=headers, params=data_dollar).json()[-1]
        
        rate = response['curs']
        CurrencyRequest.objects.create(usd_to_rub_rate=rate)
        last_request_time = now
    else:
        # Если запрос был сделан менее 10 секунд назад, используем последний сохраненный курс
        rate = CurrencyRequest.objects.last().usd_to_rub_rate

    last_10_requests = CurrencyRequest.objects.order_by('-timestamp')[:10].values('timestamp', 'usd_to_rub_rate')

    data = {
        "1_dollar": rate,
        "last_10_requests": list(last_10_requests)
    }

    return JsonResponse(data)
