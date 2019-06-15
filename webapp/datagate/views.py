from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from django.views import View

from website.models import Student, Attendance, Lesson
from datagate.models import Device

import datetime

from datagate.utils import datetimeToIndexLesson

from traceback import print_exc

import datagate.protocol as protocol

class datagate(View):
    def __init__(self):
        super().__init__()
        ver = protocol.Protocol_0_1.VERSION
        self._protocol: protocol.Protocol_0_1 = protocol.manager[ver]

    @csrf_exempt
    def get(self, request):
        now = datetime.datetime.now()
        body = self._protocol.serializeDateResponce(now)
        return HttpResponse(body)

    @csrf_exempt
    def post(self, request):
        try:
            
            cmd, obj = self._protocol.deserialize(request.body.decode())
            print('lowlevel cmd:', cmd)

            if cmd != self._protocol.NFCS_PROCESS:
                return HttpResponse(status=400)

            device, checkins = obj
            deviceObj = Device.objects.get(identifier=device)

            for nfs, date in checkins:
                nfs = nfs.decode()
                print(f"nfs: {nfs}, date: {date}")
                Log.objects.create(identifier_devices=device, identifier_card=nfs, date=date).save()

                try:
                    lessonObj = Lesson.objects.get(auditorium=deviceObj.auditorium, date=date, lesson_number=datetimeToIndexLesson(date))
                except Lesson.DoesNotExist:
                    print('Lessons not found')
                    continue

                try:
                    studentObj = Student.objects.get(identifier=nfs)
                except Student.DoesNotExist:
                    print('Student not found')
                    continue

                att, cr = Attendance.objects.get_or_create(student = studentObj, lesson = lessonObj)
                print(att, "created" if cr else "existed", att.status)

            return HttpResponse(status=200)
        except Exception:
            print("lowlevel error!")
            print_exc() 
            return HttpResponse(status=500)
