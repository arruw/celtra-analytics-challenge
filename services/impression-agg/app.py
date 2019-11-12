from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.types import StructType
from pyspark.sql.types import TimestampType
from pyspark.sql.types import LongType
from pyspark.sql.types import IntegerType

spark = SparkSession \
    .builder \
    .appName("sandbox") \
    .getOrCreate()

lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

inputDF = lines.selectExpr( \
    "cast(nvl(split(value, ' ')[0], current_timestamp()) as timestamp) as timestamp", \
    "cast(nvl(split(value, ' ')[1], 0) as long) as userId", \
    "cast(nvl(split(value, ' ')[2], 0) as long) as campaignId", \
    "cast(nvl(split(value, ' ')[3], 0) as long) as adId", \
    "cast(nvl(split(value, ' ')[4], 0) as long) as impression", \
    "cast(nvl(split(value, ' ')[5], 0) as long) as click", \
    "cast(nvl(split(value, ' ')[6], 0) as long) as touch", \
    "cast(nvl(split(value, ' ')[7], 0) as long) as swipe", \
    "cast(nvl(split(value, ' ')[8], 0) as long) as pinch")

inputDF.printSchema()

# Generate running word count
windowedCounts = inputDF \
    .groupBy("campaignId", "adId") \
    .count()

query = windowedCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()

# def parse_to_pair(line: str):
#     try:
#         tokens = tuple(map(int, line.split(" ")))
        
#         key = (tokens[2], tokens[3])
#         user = tokens[1]
#         timestamp = tokens[0]
#         metrics = {
#             0: (user, 1, 0, 0, 0, 0), # impression
#             1: (user, 0, 1, 0, 0, 0), # click
#             2: (user, 0, 0, 1, 0, 0), # pinch
#             3: (user, 0, 0, 0, 1, 0), # swipe
#             4: (user, 0, 0, 0, 0, 1)  # touch
#         }

#         metric = metrics.get(tokens[4], metrics[0])[1:] # remove user data

#         return [(key, metric)]
#     except:
#         return []


# impressions = lines.flatMap(parse_to_pair)

# impressionsAgg = impressions.reduceByKey(lambda a, b: tuple(sum(pair) for pair in zip(a, b)))

# impressionsAgg.pprint()

# ssc.start()
# ssc.awaitTermination()