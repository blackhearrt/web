
# Встановлюємо базовий образ
FROM python:3.12

# Встановлюємо робочу директорію в образі
WORKDIR /app

# Копіюємо файл main.py з локальної директорії в образ
COPY main.py /app/main.py

# Вказуємо, що треба встановити Flask
RUN pip install flask

# Запускаємо програму при запуску контейнера
CMD ["python", "main.py"]

