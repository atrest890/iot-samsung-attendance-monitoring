from django.shortcuts import render
from django.http import HttpResponseNotFound
from website.models import *
import cyrtranslit

def index(request): 
    return render(request, 'website/index.html')


def header(request):
    # faculties = {"РТФ" : "#", 
    #              "РКФ" : "#", 
    #              "ФЭТ" : "#", 
    #              "ФСУ" : "#", 
    #              "ФВС" : "#", 
    #              "ГФ" : "#", 
    #              "ЭФ" : "#", 
    #              "ФИТ" : "#", 
    #              "ЮФ" : "#", 
    #              "ФБ" : "/faculties/fb"}

    # buildings = {"УЛК" : "/buildings/ulk", 
    #              "ФЭТ" : "#", 
    #              "РК" : "#", 
    #              "ГК" : "#", 
    #              "МК" : "#"}

    faculties_obj = Faculty.objects.all()

    faculties = {}
    for obj in faculties_obj:
        name = obj.faculty_name
        latin_name = obj.latin_name
        faculties[name] = "/faculties/" + latin_name

    buildings_obj = Building.objects.all()

    buildings = {}
    for obj in buildings_obj:
        name = obj.build_name
        latin_name = obj.latin_name
        buildings[name] = "/buildings/" + latin_name

    return render(request, 'website/header.html', context = {"faculties" : faculties, "buildings" : buildings})


def faculties(request, faculty):
    if faculty == 'fb':
        courses = ["1 курс", 
                   "2 курс", 
                   "3 курс", 
                   "4 курс", 
                   "5 курс"]

        groups = {"123-4" : "fb/groups/123-4", 
                  "124-4" : "fb/groups/125-4", 
                  "126-4" : "fb/groups/123-4"}

        return render(request, 'website/fb.html', context = {"courses" : courses, "groups" : groups})
    return HttpResponseNotFound('<h1>Другие факультеты не существуют</h1>')


def groups(request, **kwargs):
    if kwargs['faculty'] == 'fb':
        if kwargs['group'] == '123-4':
            return render(request, 'website/123-4.html')
        return HttpResponseNotFound('<h1>Такой группы не существует</h1>')


def students(request, **kwargs):
    if kwargs['faculty'] == 'fb':
        if kwargs['group'] == '123-4':
            if kwargs['student'] == 'kalinin':
                return render(request, 'website/attendance_one.html')
    return HttpResponseNotFound('<h1>Такого студента не существует</h1>')


def buildings(request, building):
    if building == 'ulk':
        auditoriums = {"201" : [ None ] * (7*6), 
                       "202" : [ None ] * (7*6), 
                       "203" : [ None ] * (7*6), 
                       "211" : [ None ] * (7*6), 
                       "302" : [ None ] * (7*6), 
                       "302a" : [ None ] * (7*6), 
                       "304" : [ None ] * (7*6)
                       }

        auditoriums["201"][0] = {"name": "ТИВ", "url": "ulk/auditoriums/403/date/2019.05.05/index/1"}
        auditoriums["201"][1] = {"name": "ТИВ", "url": "#"}
        auditoriums["302"][3] = {"name": "ТИВ", "url": "#"}


        return render(request, 'website/ulk.html', context = {"auditoriums" : auditoriums})
    return HttpResponseNotFound('<h1>Такого корпуса не существует</h1>')


def lessons(request, **kwargs): #buildings/<str:building>/auditoriums/<str:auditorium>/date/<str:date>/index/<int:index>'
    if kwargs['building'] == 'ulk':
        if kwargs['auditorium'] == '403':
            if kwargs['date'] == '2019.05.05':
                if kwargs['index'] == 1:
                    return render(request, 'website/attendance_all.html')
    return HttpResponseNotFound('<h1>Такой пары не существует</h1>')