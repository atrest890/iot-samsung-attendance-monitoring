#!/usr/bin/env python3

import datetime

def timepoint(baseDate, h = 0, m = 0, s = 0):
    return baseDate.replace(hour=h, minute=m, second=s)

def datetimeToIndexLesson(date: datetime.datetime):
    timeTuple = (
        # 1: 8:50-10:25
        (timepoint(date,  8, 00), timepoint(date, 10, 24)),
        # 2: 10:40-12:15
        (timepoint(date, 10, 25), timepoint(date, 12, 14)),
        # 3: 13:15:14:50
        (timepoint(date, 13, 00), timepoint(date, 14, 49)),
        # 4: 15:00-16:35
        (timepoint(date, 14, 50), timepoint(date, 16, 34)),
        # 5: 16:45-18:20
        (timepoint(date, 16, 35), timepoint(date, 18, 19)),
        # 6: 18:30-20:05
        (timepoint(date, 18, 20), timepoint(date, 20,  4)),
        # 7: 20:15-21:50
        (timepoint(date, 20,  5), timepoint(date, 21, 49)),
    )

    for idx, (begin, end) in enumerate(timeTuple, start=1):
        if begin <= date <= end:
            return idx

def parseCheckins(checkins):
    res = []
    for card, timestamp in checkins:
        res.append((card, datetime.datetime.fromtimestamp(timestamp)))
    return res