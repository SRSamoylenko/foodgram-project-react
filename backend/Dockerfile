FROM python:3.8.5
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY foodgram .
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000