from django.shortcuts import render
from django.http import HttpResponseNotFound
from website.models import *
import cyrtranslit

def index(request): 
    return render(request, 'website/index.html')



def header(request):
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
    faculty_obj = Faculty.objects.get(latin_name = faculty)
    if not faculty_obj:
        return HttpResponseNotFound('<h1>Такого факультета не существует</h1>')

    groups_obj = Group.objects.filter(faculty_id = faculty_obj.id)
    all_groups = {}
    urls = {}
    for group in groups_obj:
        course = group.course
        group_number = group.group_number
        all_groups.setdefault(course, [])
        urls[group_number] = "/faculties/" + faculty + "/groups/" + group_number
        all_groups[course].append({"number" : group_number, "url" : urls[group_number]})
            
    print(urls)
    return render(request, 'website/faculty.html', context = { "all_groups" : all_groups })



def groups(request, **kwargs):
    faculty_obj = Faculty.objects.get(latin_name = kwargs['faculty'])
    group = Group.objects.get(group_number = kwargs['group'])

    # TODO: исправить условие

    if not faculty_obj and not groups_obj:
        return HttpResponseNotFound('<h1>Такой группы не существует</h1>')

    students_obj = Student.objects.filter(group = group.id)
    students = {}
    index = 0

    for st in students_obj:
        fio = st.surname + " " + st.name + " " + st.patronymic
        students[fio] = "/faculties/" + kwargs['faculty'] + "/groups/" + kwargs['group'] + "/students/" + str(st.id)

    return render(request, 'website/group.html', context = { "students" : students })



def students(request, **kwargs):
    # if kwargs['faculty'] == 'fb':
    #     if kwargs['group'] == '123-4':
    #         if kwargs['student'] == 'kalinin':
    #             return render(request, 'website/attendance_one.html')
    # return HttpResponseNotFound('<h1>Такого студента не существует</h1>')
    faculty_obj = Faculty.objects.get(latin_name = kwargs['faculty'])
    groups_obj = Group.objects.get(group_number = kwargs['group'])
    students_obj = Student.objects.get(id = kwargs['student_id'])

    # TODO: исправить условие

    if not students_obj:
        return HttpResponseNotFound('<h1>Такого студента не существует</h1>')

    return render(request, 'website/student.html')



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


def lessons(request, **kwargs):
    if kwargs['building'] == 'ulk':
        if kwargs['auditorium'] == '403':
            if kwargs['date'] == '2019.05.05':
                if kwargs['index'] == 1:
                    return render(request, 'website/attendance_all.html')
    return HttpResponseNotFound('<h1>Такой пары не существует</h1>')