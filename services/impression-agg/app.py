from typing import Iterator
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql import Row
from pyspark.sql import functions as fun
from mysql.connector import connect
from mysql.connector.cursor import CursorBase
from mysql.connector.pooling import PooledMySQLConnection

def getPooledConnection() -> PooledMySQLConnection:
    dbconfig = {
        "host":     "db",
        "port":     "3306",
        "database": "ads",
        "user":     "root",
        "password": "Password123!"
    }
    return connect(pool_name = "sandbox", pool_size = 16, **dbconfig)

insertStatement = "INSERT INTO `agg_daily` VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE impressions = values(impressions), interactions = values(interactions), clicks = values(clicks), uniqueUsers = values(uniqueUsers), swipes = values(swipes), pinches = values(pinches), touches = values(touches)"

def insertPartition(iterator: Iterator[Row]):
    # Get connection from connection pool
    con = getPooledConnection()
    cursor: CursorBase = con.cursor()
    needCommit = False

    # Insert records
    for r in iterator:
        row = ( \
            r["date"], \
            r["campaignId"], \
            r["adId"], \
            r["impressions"], \
            r["interactions"], \
            r["clicks"], \
            r["uniqueUsers"], \
            r["swipes"], \
            r["pinches"], \
            r["touches"], \
        )
        cursor.execute(insertStatement, row)
        needCommit = True

    # Commit and return connection
    if needCommit:
        con.commit()
    cursor.close()
    con.close()

def processBatch(df: DataFrame, batchId: int):
    df.persist()
    df.foreachPartition(insertPartition)
    df.unpersist()


spark = SparkSession \
    .builder \
    .appName("snadbox") \
    .getOrCreate()

# Read structured stream from socket and apply schema
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "impressions-gen") \
    .option("port", 9999) \
    .load()

inputDF = lines.selectExpr( \
    "cast(split(value, ' ')[0] as timestamp) as timestamp", \
    "cast(split(value, ' ')[1] as long) as userId", \
    "cast(split(value, ' ')[2] as long) as campaignId", \
    "cast(split(value, ' ')[3] as long) as adId", \
    "cast(split(value, ' ')[4] as long) as impression", \
    "cast(split(value, ' ')[5] as long) as click", \
    "cast(split(value, ' ')[6] as long) as touch", \
    "cast(split(value, ' ')[7] as long) as swipe", \
    "cast(split(value, ' ')[8] as long) as pinch")

# Prepare aggregation query
windowedCounts = inputDF \
    .withWatermark("timestamp", "1 hour") \
    .groupBy(fun.window("timestamp", "24 hour"), "campaignId", "adId") \
    .agg( \
        fun.sum("impression").alias("impressions"), \
        fun.sum("click").alias("clicks"), \
        fun.sum("touch").alias("touches"), \
        fun.sum("swipe").alias("swipes"), \
        fun.sum("pinch").alias("pinches"), \
        fun.approx_count_distinct("userId").alias("uniqueUsers") \
    ) \
    .select(fun.col("window.start").cast("date").alias("date"), "*") \
    .drop("window")

windowedCounts = windowedCounts \
    .withColumn("interactions", sum([windowedCounts["touches"], windowedCounts["swipes"], windowedCounts["pinches"]]))

windowedCounts = windowedCounts \
    .withColumn("impressions", sum([windowedCounts["impressions"], windowedCounts["interactions"]]))

# Start the stream, sink changed rows to MySQL database, trigger every 1 minute
query = windowedCounts \
    .writeStream \
    .foreachBatch(processBatch) \
    .outputMode("update") \
    .start()

    # TODO: this doens't work
    # .trigger(continuous="60 seconds") \

query.awaitTermination()