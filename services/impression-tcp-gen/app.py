import socket
import time
import random
import datetime

host = ''
port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

def generateImpression(c,a,u,i):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    campaignId = random.randint(1, c)
    adId = random.randint(1, a)
    userId = random.randint(1, u)
    eventId = random.randint(1, i) 

    events = {
        0: "1 0 0 0 0", # impression
        1: "0 1 0 0 0", # click
        2: "0 0 1 0 0", # touch
        3: "0 0 0 1 0", # swipe
        4: "0 0 0 0 1"  # pinch
    }

    impression = f"{timestamp} {userId} {campaignId} {adId} {events.get(eventId, events[0])}"

    print(impression, flush=True)

    return f"{impression}\n"


try:
    while True:
        conn, addr = s.accept()
        try:
            while True:
                conn.send(bytes(generateImpression(10, 20, 100, 5), "utf-8"))
                time.sleep(0.05)
            conn.close()
        except socket.error:
            print("Error")
            pass
finally:
    s.close()