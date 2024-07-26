FROM python:3-slim
WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

CMD ["gunicorn", "WebPOS.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "2"]
