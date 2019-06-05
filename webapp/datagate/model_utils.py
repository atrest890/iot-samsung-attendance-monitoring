#!/usr/bin/env python3

from datagate.models import Log

def logging(devices, checkins):
    for card, date in checkins:
        Log.objects.create(identifier_devices=devices, identifier_card=card, date=date).save()
