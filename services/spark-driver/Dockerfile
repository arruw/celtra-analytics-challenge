FROM bde2020/spark-submit:2.4.1-hadoop2.7

ENV ENABLE_INIT_DAEMON=false

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY app.py /app/app.py
