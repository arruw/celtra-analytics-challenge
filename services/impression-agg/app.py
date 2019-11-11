import pyspark

spark = pyspark.sql.SparkSession.builder.appName("test").getOrCreate()
sc: pyspark.sql.SparkSession = spark.sparkContext

campaignDF = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://db:3306/ads") \
    .option("dbtable", "ads.campaign") \
    .option("user", "root") \
    .option("password", "Password123!") \
    .load()

adDF = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://db:3306/ads") \
    .option("dbtable", "ads.ad") \
    .option("user", "root") \
    .option("password", "Password123!") \
    .load()

impressionDF = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://db:3306/ads") \
    .option("dbtable", "ads.impression") \
    .option("user", "root") \
    .option("password", "Password123!") \
    .load()

campaignDF.createTempView("campaign")
adDF.createTempView("ad")
impressionDF.createTempView("impression")

aggDF = spark.sql("""
    SELECT
        DATE(i.date) AS `date`
        ,c.id AS `campaign_id`
        ,a.id AS `ad_id`
        ,c.name AS `campaign_name`
        ,a.name AS `ad_name`
        ,COUNT(*) AS `impressions`
        ,SUM(i.click)+SUM(i.swipe)+SUM(i.pinch)+SUM(i.touch) AS `interactions`
        ,SUM(i.click) AS `clicks`
        ,COUNT(DISTINCT i.id_user) AS `uniqueUsers`
        ,SUM(i.swipe) AS `swipes`
        ,SUM(i.pinch) AS `pinches`
        ,SUM(i.touch) AS `touches`
    FROM campaign AS c
    INNER JOIN ad AS a ON a.id_campaign = c.id
    INNER JOIN impression AS i ON i.id_ad = a.id
    GROUP BY DATE(i.date), c.id, a.id, c.name, a.name""")

aggDF.write.format("jdbc") \
    .option("url", "jdbc:mysql://db:3306/ads") \
    .option("dbtable", "ads.agg_daily") \
    .option("user", "root") \
    .option("password", "Password123!") \
    .mode("overwrite") \
    .save()

spark.stop()