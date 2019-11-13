from pyspark.sql import SparkSession
from pyspark.sql import functions as fun

spark = SparkSession \
    .builder \
    .appName("sandbox") \
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
    .groupBy(fun.window("timestamp", "24 hour"), "campaignId", "userId") \
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

# Start the stream, output only changed rows, trigger every minute
query = windowedCounts \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

    # TODO: this doens't work
    # .trigger(continuous="60 seconds") \

    # TODO: write cusom sink for MySQL database, upsert records

query.awaitTermination()