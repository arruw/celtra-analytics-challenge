FROM python:3-alpine
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/app.py

EXPOSE 9999

ENTRYPOINT [ "python", "/app/app.py"]
