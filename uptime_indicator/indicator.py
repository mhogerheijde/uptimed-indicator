# coding=UTF-8

from .uptime import UptimeRecords
from datetime import timedelta
from termcolor import colored

lunchDelta = timedelta(minutes=30)
workDayDelta = timedelta(hours=8)


def main():
    uptimeRecords = UptimeRecords()
    records = uptimeRecords.read()
    previous_week = None
    total_uptime = {
        date.isocalendar()[1]: {'total': timedelta(0), 'daysWorked': 0} for date in records.keys()}

    total_overtime = timedelta()

    for key in records:
        (_, current_week, _) = key.isocalendar()
        (boot, down, uptime) = records[key]

        if previous_week is not None and previous_week != current_week:
            print "-" * 80
            printCummulatives(previous_week, total_uptime)
            print "-" * 80

        dayOvertimeDelta = (uptime - (workDayDelta + lunchDelta))
        total_overtime += dayOvertimeDelta

        print u"{} ({}): |{} → {}| {} / {} ({:>5}) ({})".format(
            key.strftime("%Y-%m-%d (%a)"),
            current_week,
            boot.strftime("%H:%M"),
            down.strftime("%H:%M"),
            uptime,
            afterLunch(uptime),
            fromatAsDecimalHours(afterLunch(uptime)),
            fromatAsHoursMinutes(delta = dayOvertimeDelta, leadingPlusActive=True))

        total_uptime[current_week]['total'] += uptime
        total_uptime[current_week]['daysWorked'] += 1
        previous_week = current_week

    printCummulatives(current_week, total_uptime)
    print "-" * 80
    print "total overtime: {}".format(fromatAsHoursMinutes(total_overtime, leadingPlusActive=True))


def afterLunch(delta):
    if delta < lunchDelta:
        return delta
    else:
        return delta - lunchDelta


def calculateExpectedDelta(week, totals):
    daysWorked = totals[week]['daysWorked']
    return (workDayDelta * daysWorked) + (lunchDelta * daysWorked)


def calculateOvertime(week, totals):
    actualDelta = totals[week]['total']
    expectedDelta = calculateExpectedDelta(week, totals)
    return (actualDelta - expectedDelta)


def printCummulatives(week, totals):
    actualDelta = totals[week]['total']
    daysWorked = totals[week]['daysWorked']

    overtimeDelta = calculateOvertime(week, totals)

    cummulative = fromatAsHoursMinutes(actualDelta)
    overtime = fromatAsHoursMinutes(delta=overtimeDelta, leadingPlusActive=True)

    print " -> Week {} (days: {}) | {} | overtime: {}".format(week, daysWorked, cummulative, overtime)


def fromatAsDecimalHours(delta):
    return "{:.2f}".format(round(delta.total_seconds() / 3600, 2))


def fromatAsHoursMinutes(delta, leadingPlusActive=False, includeSeconds=False):
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

    formatted = "{2}{0:02d}:{1:02d}".format(hours, minutes, "-" if isNegative else leadingPlus)
    if includeSeconds:
        formatted = "{3}{0:02d}:{1:02d}:{2:02d}".format(hours, minutes, seconds, "-" if isNegative else leadingPlus)

    if leadingPlusActive:
        color = 'red' if isNegative else 'green'
        return colored(formatted, color)
    else:
        return formatted

if __name__ == "main":
    main()
