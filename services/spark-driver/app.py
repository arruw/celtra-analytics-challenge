from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test").getOrCreate()

data = spark.sparkContext.parallelize(range(1, 10))

data = data.map(lambda x: x*x).collect()

print(data)

spark.stop()