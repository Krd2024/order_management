# Приложение для управления заказами

## Возможности
Приложение позволяет:
- Добавлять, удалять, искать, изменять и отображать заказы.
- Использовать интуитивно понятный интерфейс.

## Создание заказа
1. Добавить необходимое количество блюд с ценами (список добавленных блюд отобразится сразу).
2. Указать номер стола и сохранить заказ.

## Управление заказами
- **Кнопка "Список заказов"** — отображает все заказы с информацией:
  - Номер заказа (ID)
  - Номер стола
  - Статус заказа
  - Возможность редактирования (статуса, номера стола)
  - Возможность удаления заказа
- При нажатии на заказ открывается окно с деталями:
  - Номер стола
  - Статус заказа
  - Общая сумма заказа
  - Перечень блюд с ценами
  - Возможность добавить/удалить блюдо из заказа

## Поиск заказов
Поиск возможен по:
- Номеру заказа
- Номеру стола
- Статусу заказа

## Выручка
- **Кнопка "Выручка"** — отображает текущую выручку всех заказов со статусом "Оплачено".

---
# Установка и запуск

1.Склонируйте репозиторий:
   ```bash
git clone https://github.com/Krd2024/order_management.git
```
2.Создание виртуального окружения
```bash
python -m venv .venv
```
3.Активация виртуального окружения
```bash
.venv\Scripts\activate
```
4.Установка зависимостей проекта
```bash
pip install -r requirements.txt
```

**Создать файл .env**
Добавьте соответствующие значения в .env файл:
```python
SECRET_KEY=django-insecure-krzw4%tx1j9jnfjlup5@#zo00#ffn12pvd6+jg$fsb831o%5a0
```
5.Миграции
```bash
python manage.py migrate
```
6.Запуск
```bash
python manage.py runserver
```
# После запуска проекта API для работы с приложение доступно:
```bash
http://127.0.0.1:8000/api/v1/docs/
```
# Запуск тестов
```bash
pytest -v
```
---

![2025-02-09_17-19-39](https://github.com/user-attachments/assets/c211f0dc-7765-420d-9e28-f092cfe2486b)

---
![2025-![2025-02-11_09-55-44](https://github.com/user-attachments/assets/9d934647-bd1e-4fa6-beb3-e15ecc33f9ac)

---
![2025-02-09_20-50-27](https://github.com/user-attachments/assets/0f78e4db-353f-460d-b95a-fb9cea0bec8d)

---
![2025-02-10_14-55-41](https://github.com/user-attachments/assets/82501b80-8e32-4ecf-93e8-34ec5d3d3c5d)

---
![2025-02-09_10-47-13](https://github.com/user-attachments/assets/f28033ca-f920-480e-b65b-ca7d24cae1c8)

---
![http___127 0 0 1_8000_api_v1_orders_ - FastAPI_test 10 02 2025 19_27_42](https://github.com/user-attachments/assets/f33eb80c-786b-41b3-8a22-39fb45f30cea)
![http___127 0 0 1_8000_api_v1_orders_3_ - FastAPI_test 10 02 2025 19_42_45](https://github.com/user-attachments/assets/0d94025f-1ee6-4435-9186-8c3c7a5e44b4)
