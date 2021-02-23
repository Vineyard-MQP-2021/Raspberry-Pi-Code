import glob
import os
import base64
from pymongo import MongoClient
import api_keys
import datetime
import time


files = glob.glob('/home/pi/Documents/motion/*')
latest = max(files, key=os.path.getctime)

with open(latest, "rb") as f:
    encoded = base64.b64encode(f.read())
    client = MongoClient(api_keys.mongodb)
    date = datetime.date.today().strftime("%A %b. %d").upper()
    time = time.strftime("%H:%M")
    db = client['Motion']
    doc = {"date": date,"time": time, "b64": encoded}
    db['detections'].insert(doc)
    f.close()
