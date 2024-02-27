# Используем базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и файлы проекта в контейнер
COPY requirements.txt .
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Определяем команду запуска приложения в контейнере
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
