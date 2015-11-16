from .uptime import UptimeRecords
from datetime import timedelta

lunchDelta = timedelta(minutes=30)


def main():
    uptimeRecords = UptimeRecords()
    records = uptimeRecords.read()
    previous_week = None
    total_uptime = {
        date.isocalendar()[1]: {'total': timedelta(0), 'daysWorked': 0} for date in records.keys()}
    for key in records:
        (_, current_week, _) = key.isocalendar()
        (boot, down, uptime) = records[key]

        if previous_week is not None and previous_week != current_week:
            printCummulatives(previous_week, total_uptime)

        print "{} ({}): {} / {}".format(key.strftime("%Y-%m-%d (%a)"), current_week, uptime, afterLunch(uptime))

        total_uptime[current_week]['total'] += uptime
        total_uptime[current_week]['daysWorked'] += 1
        previous_week = current_week

    printCummulatives(current_week, total_uptime)


def afterLunch(delta):
    if delta < lunchDelta:
        return delta
    else:
        return delta - lunchDelta


def printCummulatives(week, totals):
    actualDelta = totals[week]['total']
    daysWorked = totals[week]['daysWorked']
    expectedDelta = timedelta(hours=8*totals[week]['daysWorked'], minutes=30*totals[week]['daysWorked'])

    cummulative = fromatAsHoursMinutes(actualDelta)
    overtime = fromatAsHoursMinutes(delta=(actualDelta - expectedDelta), leadingPlusActive=True)
    print " -> Week {} (days: {}) | {} | overtime: {}".format(week, daysWorked, cummulative, overtime)


def fromatAsHoursMinutes(delta, leadingPlusActive=False):
    isNegative = False
    if delta < timedelta():
        delta = delta * -1
        isNegative = True

    leadingPlus = ""
    if leadingPlusActive:
        leadingPlus = "+"

    hours = delta.days * 24 + delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = (delta.seconds % 3600) % 60
    return "{3}{0:02d}:{1:02d}:{2:02d}".format(hours, minutes, seconds, "-" if isNegative else leadingPlus)

if __name__ == "main":
    main()
