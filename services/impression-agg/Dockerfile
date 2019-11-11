FROM bde2020/spark-submit:2.4.1-hadoop2.7

ENV ENABLE_INIT_DAEMON=false

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.18.tar.gz \
    && tar xvf mysql-connector-java-8.0.18.tar.gz \
    && rm mysql-connector-java-8.0.18.tar.gz

COPY app.py /app/app.py

ENV SPARK_SUBMIT_ARGS="--driver-class-path mysql-connector-java-8.0.18/mysql-connector-java-8.0.18.jar --jars mysql-connector-java-8.0.18/mysql-connector-java-8.0.18.jar"