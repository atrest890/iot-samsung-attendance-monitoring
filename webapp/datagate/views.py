from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from website.models import Student, Attendance, Lesson
from datagate.models import Device

import datetime
import json

from datagate.utils import datetimeToIndexLesson, parseCheckins
from datagate.model_utils import logging

@csrf_exempt
def lowlevel(request):
    try:
        if request.method == 'GET':
            dt = datetime.datetime.now()
            return HttpResponse(str(dt.timestamp()).encode())

        if request.method != 'POST':
            return HttpResponseNotAllowed(["GET", "POST"])
        
        device, rowCheckins = json.loads(request.body.decode())
        checkins = parseCheckins(rowCheckins)

        logging(device, checkins)
        
        deviceObj = Device.objects.get(identifier = device)

        for nfs, date in checkins:
            print(f"nfs: {nfs}, date: {date}")

            lessonObj = Lesson.objects.get(auditorium = deviceObj.auditorium, lesson_number = datetimeToIndexLesson(date))
            studentObj = Student.objects.get(identifier=nfs)

            # TODO: разобраться с дублирующимися чекинами
            Attendance.objects.create(student = studentObj, lesson = lessonObj).save()

        return HttpResponse(status=200)
    except Exception as e:
        print("lowlevel error!")
        print(e)
        return HttpResponse(status=500)