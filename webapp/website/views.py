from django.shortcuts import render
from django.http import HttpResponseNotFound

def index(request):    
    return render(request, 'website/index.html')

def header(request):
    return render(request, 'website/header.html')

def faculties(request, faculty):
    if faculty == 'fb':
        return render(request, 'website/fb.html')
    return HttpResponseNotFound('<h1>Другие факультеты не существуют</h1>')

def buildings(request, building):
    if building == 'ulk':
        return render(request, 'website/ulk.html')
    return HttpResponseNotFound('<h1>Такого корпуса не существует</h1>')


def lessons(request, **kwargs): #buildings/<str:building>/auditoriums/<str:auditorium>/date/<str:date>/index/<int:index>'
    if kwargs['building'] == 'ulk':
        if kwargs['auditorium'] == '403':
            if kwargs['date'] == '2019.05.05':
                if kwargs['index'] == 1:
                    return render(request, 'website/attendance_all.html')
    return HttpResponseNotFound('<h1>Такой пары не существует</h1>')