import mysql.connector
import os
import random
import datetime

def connect():
    host = os.environ.get("MYSQL_HOST", "localhost")
    port = os.environ.get("MYSQL_PORT", "3306")
    db = os.environ.get("MYSQL_DATABASE", None)
    user = os.environ.get("MYSQL_USER", "root")
    passwd = os.environ.get("MYSQL_PASSWD", None)

    con = mysql.connector.connect(
        host=host,
        port=port,
        db=db,
        user=user,
        passwd=passwd
    )

    return con

def getNextId(cursor: mysql.connector.cursor.MySQLCursor, table):
    query = ("SELECT COUNT(*) AS prevId FROM `" + table + "`")
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0]+1 if len(result) == 1 else 1

def insertCampaign(cursor: mysql.connector.cursor.MySQLCursor, params):
    cursor.execute("INSERT INTO `campaign` (`name`) VALUES (%s)", params)
    cursor.close()

def insertAd(cursor: mysql.connector.cursor.MySQLCursor, params):
    cursor.execute("INSERT INTO `ad` (`id_campaign`, `name`) VALUES (%s, %s)", params)
    cursor.close()

def insertImpression(cursor: mysql.connector.cursor.MySQLCursor, params):
    cursor.execute(f"INSERT INTO `impression` VALUES (%s, %s, %s, %s, %s, %s, %s)", params)
    cursor.close()

con = connect()

campaignNextId = getNextId(con.cursor(), "campaign")
adNextId = getNextId(con.cursor(), "ad")

print("Inserting campaigns...")
for _ in range(10):
    insertCampaign(con.cursor(), (f"camp_{campaignNextId}", ))
    insertAd(con.cursor(), (campaignNextId, f"ad_{adNextId}", ))
    campaignNextId += 1
    adNextId += 1
con.commit()

print("Inserting ads...")
for _ in range(20):
    campaignId = random.randint(1, campaignNextId - 1)
    insertAd(con.cursor(), (campaignId, f"ad_{adNextId}"))
    adNextId += 1
con.commit()

print("Inserting impressions...")
for _ in range(100):
    adId = random.randint(1, adNextId - 1)
    userId = random.randint(1, 10000)
    date = datetime.datetime.now() - datetime.timedelta(minutes=random.randint(1, 60))
    touch = 0
    pinch = 0
    swipe = 0
    click = 0
    if random.randint(1, 10) > 8:
        touch = random.randint(0,4)
        pinch = random.randint(0,3)
        swipe = random.randint(0,3)
    
        if random.randint(1, 10) > 5: 
            click = random.randint(0,2)
    insertImpression(con.cursor(), (adId, userId, date, click, touch, pinch, swipe))
con.commit()
print("Done.")