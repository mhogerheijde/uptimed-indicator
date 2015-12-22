# coding=UTF-8

from .uptime import UptimeRecords
from datetime import timedelta, date
from dateutil.parser import parse
from termcolor import colored

lunchDelta = timedelta(minutes=30)
workDayDelta = timedelta(hours=8)


def main():

    offsets = {
        parse('2015-12-08').date(): timedelta(hours = -1.75)
    }

    uptimeRecords = UptimeRecords()
    records = uptimeRecords.read(offsets)
    previous_week = None
    total_uptime = {date.isocalendar()[1]: {'total': timedelta(0), 'daysWorked': 0} for date in records.keys()}

    total_overtime = timedelta(hours=-6.5)  # Initial offset first workweek

    (_, actual_week_number, _) = date.today().isocalendar()

    print "-" * 80
    print " -> Offset {}".format(fromatAsHoursMinutes(total_overtime, leadingPlusActive=True))
    print "-" * 80

    for key in records:
        (_, current_week, _) = key.isocalendar()
        (boot, down, uptime) = records[key]
        detail_previous = actual_week_number - current_week < 1
        detail_current = actual_week_number - current_week < 2

        if previous_week is not None and previous_week != current_week:
            if detail_previous:
                print "-" * 80
            printCummulatives(previous_week, total_uptime)
            if detail_current:
                print "-" * 80

        dayOvertimeDelta = (uptime - (workDayDelta + lunchDelta))
        total_overtime += dayOvertimeDelta

        if detail_current:
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

    print "-" * 80
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

    print u" -> Week {} (days: {}) | {} | overtime: {}".format(week, daysWorked, cummulative, overtime)


def fromatAsDecimalHours(delta):
    return "{:.2f}".format(round(delta.total_seconds() / 3600, 2))


def fromatAsHoursMinutes(delta, leadingPlusActive=False, includeSeconds=False):
    isNegative = False
    if delta < timedelta():
        delta = delta * -1
        isNegative = True

    leadingPlus = u""
    if leadingPlusActive:
        leadingPlus = u"+"

    hours = delta.days * 24 + delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    seconds = (delta.seconds % 3600) % 60

    formatted = u"{2}{0:02d}:{1:02d}".format(hours, minutes, "-" if isNegative else leadingPlus)
    if includeSeconds:
        formatted = u"{3}{0:02d}:{1:02d}:{2:02d}".format(hours, minutes, seconds, "-" if isNegative else leadingPlus)

    if leadingPlusActive:
        color = 'red' if isNegative else 'green'
        return colored(formatted, color)
    else:
        return formatted

if __name__ == "main":
    main()
