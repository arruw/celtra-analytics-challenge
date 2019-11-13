from typing import Iterator
from pyspark.sql import DataFrame
from pyspark.sql import Row
from mysql.connector import connect
from mysql.connector.cursor import CursorBase
from mysql.connector.pooling import PooledMySQLConnection

def getPooledConnection() -> PooledMySQLConnection:
    dbconfig = {
        "host":     "localhost",
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