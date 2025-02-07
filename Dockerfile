FROM python:3.12
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requarements.txt requarements.txt
RUN pip install --upgrade pip
RUN pip install -r requarements.txt
COPY mysite .

#RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
