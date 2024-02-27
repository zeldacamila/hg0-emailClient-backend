FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate

EXPOSE 8000

ENV SECRET_KEY=$SECRET_KEY
ENV DEBUG=$DEBUG
ENV DB_NAME=$DB_NAME
ENV DB_USER=$DB_USER
ENV DB_PASSWORD=$DB_PASSWORD
ENV DB_HOST=$DB_HOST
ENV DB_PORT=$DB_PORT
ENV ALLOWED_HOSTS=$ALLOWED_HOSTS

CMD ["gunicorn", "emailClient.wsgi:application", "--bind", "0.0.0.0:8000"]