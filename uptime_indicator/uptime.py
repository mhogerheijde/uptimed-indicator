import os.path
import csv
from datetime import datetime, timedelta
from collections import OrderedDict


UPRECORDS_FILE = os.path.join("/", "var", "spool", "uptimed", "records")
FIELDNAMES = ['uptime', 'boottime', 'kernel']


class UptimeRecords(object):

    def __init__(self):
        pass

    # TODO: This method does not correctly handle day-boundaries
    def read(self, offsets):

        print offsets

        with open(UPRECORDS_FILE, 'r') as csvfile:
            data = csv.DictReader(csvfile, fieldnames=FIELDNAMES, delimiter=':')

            records = {}
            for row in data:
                bootDateTime = datetime.fromtimestamp(int(row['boottime']))
                downDateTime = bootDateTime + timedelta(seconds=int(row['uptime']))

                bootDate = bootDateTime.date()
                newBootDateTime = bootDateTime
                newDownDateTime = downDateTime
                if bootDate in records:
                    (existingBootDateTime, existingDownDateTime, exsitingUptimeDelta) = records[bootDate]

                    if (bootDateTime > existingBootDateTime):
                        newBootDateTime = existingBootDateTime

                    if (downDateTime < existingDownDateTime):
                        newDownDateTime = existingDownDateTime

                offsetDelta = offsets[bootDate] if bootDate in offsets else timedelta()
                newUptimeDelta = newDownDateTime - newBootDateTime + offsetDelta

                records[bootDate] = (newBootDateTime, newDownDateTime, newUptimeDelta)

        return OrderedDict(sorted(records.iteritems()))

