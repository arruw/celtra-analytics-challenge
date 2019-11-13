FROM bde2020/spark-submit:2.4.4-hadoop2.7

ENV ENABLE_INIT_DAEMON=false

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/app.py