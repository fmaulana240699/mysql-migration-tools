FROM python:3.10-slim

WORKDIR /app

RUN apt update && apt install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
