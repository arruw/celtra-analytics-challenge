import mysql.connector
import os
import sys
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

def insert(con: mysql.connector.connection.MySQLConnection, createCampaigns, createAds, createImpressions, days=1):
    campaignNextId = getNextId(con.cursor(), "campaign")
    adNextId = getNextId(con.cursor(), "ad")
    
    for i in range(days, 0, -1):
        campaignStartId = campaignNextId
        adStartId = adNextId

        day = datetime.date.today() - datetime.timedelta(days=i-1)
        print(f"Generating for date: {day}", flush=True)

        print(f"\tGenerating {createCampaigns} campaigns...", flush=True)
        for _ in range(createCampaigns):
            insertCampaign(con.cursor(), (f"camp_{campaignNextId}", ))
            insertAd(con.cursor(), (campaignNextId, f"ad_{adNextId}", ))
            campaignNextId += 1
            adNextId += 1
        con.commit()

        print(f"\tGenerating {createAds} ads...", flush=True)
        for _ in range(createAds):
            campaignId = random.randint(campaignStartId, campaignNextId - 1)
            insertAd(con.cursor(), (campaignId, f"ad_{adNextId}"))
            adNextId += 1
        con.commit()

        print(f"\tGenerating {createImpressions} impressions...", flush=True)
        for _ in range(createImpressions):
            tmpAdStartId = adStartId if random.randint(1,10) > 6 else 1
            adId = random.randint(tmpAdStartId, adNextId - 1)
            userId = random.randint(1, 10000)
            date = datetime.datetime.combine(day, datetime.datetime.min.time()) + datetime.timedelta(seconds=random.randint(1, 86400))
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

    print("Done.", flush=True)





con = connect()

createCampaigns = 20
createAds = createCampaigns*3
createImpressions = createAds*50
days = 1

if len(sys.argv) == 2:
    days = int(sys.argv[1])

insert(con, createCampaigns, createAds, createImpressions, days)