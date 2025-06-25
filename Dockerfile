
FROM python:3.10.2-slim-buster

LABEL authors="grape"

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY server.py .
EXPOSE 15000
ENTRYPOINT ["python", "server.py"]