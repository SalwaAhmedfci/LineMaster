FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000
# Ensure Memcached communication via environment variables (Optional)
ENV MEMCACHED_HOST=memcached MEMCACHED_PORT=11211

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
