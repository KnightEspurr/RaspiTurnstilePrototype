import time
from datetime import datetime, timedelta
from allmyfunctions import *
print("Delete scheduler activated! This operation will repeat every 15 minutes")
while True:
    print(str(datetime.now()))
    deleteExpiredRecords()
    time.sleep(interval)
