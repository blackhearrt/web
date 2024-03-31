FROM python:3.9

RUN pip install Flask python-socketio

WORKDIR /app

COPY . .

RUN mkdir -p /app/storage

RUN touch /app/storage/data.json

CMD ["python", "main.py"]
