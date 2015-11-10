from .uptime import UptimeRecords
from datetime import timedelta

def main():
    uptimeRecords = UptimeRecords()
    records = uptimeRecords.read()
    for key in records:
        (_, _, uptime) = records[key]
        print "{}: {}".format(key.strftime("%Y-%m-%d (%a)"), uptime - timedelta(minutes=30))

if __name__ == "main":
    main()
