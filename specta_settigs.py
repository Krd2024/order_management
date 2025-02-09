SPECTACULAR_SETTINGS = {
    "TITLE": "API для CRUD операций ",
    "DESCRIPTION": """
        Этот API предоставляет функции для работы с заказами включая:

        - Создания заказ с блюдами
        - Просмотр списока всех заказов
        - Просмотр одного заказа по ID
        - Обновление заказа по ID
        - Удаление заказа по ID

        Пример запроса для внешних запросов:

        Для отправки POST-запроса:


        #URL для запроса
        url = 'http://127.0.0.1:8080/api/v1/orders/'
        

        # Данные для отправки (IMEI для проверки)
        data = {
                    "table_number": 10,
                    "status": "pending", 
                    "items": [
                        {"product_name": "Суп", "price": 250.0},
                        {"product_name": "Салат", "price": 200.0},
                        {"product_name": "Компот", "price": 100.0},
                    ],
                },

        # Заголовки 
        headers = {
            'Content-Type': 'application/json'  
        }

        # Отправка POST-запроса
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Проверка ответа
        if response.status_code == 201:
            print('Успешный запрос:', response.json())
        else:
            print('Ошибка:', response.status_code, response.text)
        
        
    """,
    "VERSION": "1.0",
}
