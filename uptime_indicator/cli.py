# coding=UTF-8

from .uptime import UptimeRecords
from datetime import timedelta, date
from dateutil.parser import parse
from termcolor import colored

lunchDelta = timedelta(minutes=30)
workDayDelta = timedelta(hours=8)

verbose = False


def main():
    offsets = {
        # Don't remember
        parse('2015-12-08').date(): timedelta(hours = -1.75),
        # Nieuwjaarsborrel
        parse('2016-01-21').date(): timedelta(hours = -1),
        # Realisatieoverleg
        parse('2016-01-28').date(): timedelta(hours = 3)
    }

    uptimeRecords = UptimeRecords()
    records = uptimeRecords.read(offsets)
    previous_key = None
    total_uptime = {uptimeKeyForDate(date): {'total': timedelta(0), 'daysWorked': 0} for date in records.keys()}

    total_overtime = timedelta(hours=-6.5)  # Initial offset first workweek

    (actual_year, actual_week_number, _) = date.today().isocalendar()

    print "-" * 80
    print " → Offset {}".format(fromatAsHoursMinutes(total_overtime, leadingPlusActive=True))
    print "-" * 80

    for key in records:

        current_key = uptimeKeyForDate(key)
        (current_year, current_week, _) = key.isocalendar()

        if (current_year < actual_year):
            current_week = current_week - weeksForYear(current_year)

        (boot, down, uptime, dayOffset) = records[key]
        detail_previous = actual_week_number - current_week < 1 or verbose
        detail_current = actual_week_number - current_week < 2 or verbose

        if previous_key is not None and previous_key != current_key:
            if detail_previous:
                print "-" * 80
            printCummulatives(previous_key, total_uptime)
            if detail_current:
                print "-" * 80

        dayOvertimeDelta = (uptime - (workDayDelta + lunchDelta))
        total_overtime += dayOvertimeDelta

        if detail_current:
            print u"{} ({}): |{} → {}| {} / {} ({:>5}) ({}){}".format(
                key.strftime("%Y-%m-%d (%a)"),
                current_week,
                boot.strftime("%H:%M"),
                down.strftime("%H:%M"),
                uptime,
                afterLunch(uptime),
                fromatAsDecimalHours(afterLunch(uptime)),
                fromatAsHoursMinutes(delta = dayOvertimeDelta, leadingPlusActive=True),
                formatOffset(dayOffset)
                )

        total_uptime[current_key]['total'] += uptime
        total_uptime[current_key]['daysWorked'] += 1
        previous_key = current_key

    print "-" * 80
    printCummulatives(current_key, total_uptime)
    print "-" * 80
    print "total overtime: {}".format(fromatAsHoursMinutes(total_overtime, leadingPlusActive=True))


def formatOffset(offset):
    if (offset > timedelta(minutes=0)):
        return " ({})".format(fromatAsHoursMinutes(delta = offset, leadingPlusActive=True))
    else:
        return ""


def weeksForYear(year):
    """
       Implementation is based upon the special property of the last week
       that states that it always has december 28 in it.
       See https://en.wikipedia.org/wiki/ISO_week_date#Last_week
    """
    (_, weeknumber, _) = date(year, 12, 28).isocalendar()
    return weeknumber


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

    print u" → Week {} (days: {}) | {} | overtime: {}".format(week, daysWorked, cummulative, overtime)


def fromatAsDecimalHours(delta):
    return "{:.2f}".format(round(delta.total_seconds() / 3600, 2))


def uptimeKeyForDate(date):
    (year, weeknumber, _) = date.isocalendar()
    return "{}-{}".format(year, weeknumber)


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
