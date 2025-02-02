FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requarement.txt requarement.txt
RUN pip install --upgrade pip
RUN pip install -r requarement.txt
COPY django_dz/django_dz .

CMD ["gunicorn", "django_dz.wsgi:application", "--bind", "0.0.0.0:8000"]