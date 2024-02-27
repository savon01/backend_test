import time
import random

from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin, ModelView

from database import create_request, update_result, get_history, engine
from database import Request

app = FastAPI(title="My Custom Documentation")

# админка
admin = Admin(engine)
admin.add_view(ModelView(Request))
admin.mount_to(app)


def emulate_external_server(request_id: int):
    """
    Работа дополнительного сервера
    :param request_id: id записи в бд
    """
    delay = random.randint(0, 60)
    # ждем заданное время
    time.sleep(delay)
    result = random.choice([True, False])

    # Сохранение результата в базе данных
    update_result(request_id, result)


@app.get("/ping")
def ping():
    """
    Проверка работы сервера
    :return: Словарь с записью о работе сервера
    """
    return {"message": "Server is running"}


@app.post("/query")
def process_query(cadastre_number: str, latitude: float, longitude: float):
    """
    Создание записи в бд
    :param cadastre_number: Кадастровый номер
    :param latitude: Широта
    :param longitude: Долгота
    :return: Словарь с идентификатором запроса
    """
    request_id = create_request(cadastre_number, latitude, longitude)
    emulate_external_server(request_id)

    return {"request_id": request_id}


@app.put("/result")
def update_query_result(request_id: int, result: bool):
    """
    Обнавление в бд результата работы сервера по id записи
    :param request_id: id записи
    :param result: Булевое значение работы сервера (true или false)
    :return: Словарь с сообщением Result updated successfully
    """
    update_result(request_id, result)
    return {"message": "Result updated successfully"}


@app.get("/history")
def get_query_history(cadastre_number: str = None):
    """
    Получение истории запросов по кадастровому номеру или всех запросов, если номер не указан
    :param cadastre_number: Кадастровый номер
    :return: Словарь history
    """
    history = get_history(cadastre_number)
    return {"history": history}



