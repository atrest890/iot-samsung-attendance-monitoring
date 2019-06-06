from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.views import View
import django.contrib.auth as auth

from website.models import Student, Faculty, Auditorium, Building, Group, Group_Lesson, Lesson, Professor, Attendance
import website.model_utils as mu

import cyrtranslit
from datetime import datetime, date, timedelta


def index(request): 
    return render(request, 'website/index.html')



def header(request):
    FacultyObjList = Faculty.objects.all()

    faculties = {}
    for obj in FacultyObjList:
        name = obj.faculty_name
        latin_name = obj.latin_name
        faculties[name] = f"/faculties/{latin_name}"

    BuildingObjList = Building.objects.all()

    buildings = {}

    for obj in BuildingObjList:
        name = obj.build_name
        latin_name = obj.latin_name
        buildings[name] = f"/buildings/{latin_name}"

    acc = {'fullname': '', 'profile_url' : '#' }
    if request.user.is_authenticated:
        acc['fullname'] = mu.getAccauntName(request.user)

    return render(request, 'website/header.html', context = {"faculties" : faculties, 
                                                             "buildings" : buildings,
                                                             "acc" : acc})



def faculties(request, faculty):
    FacultyObj = Faculty.objects.get(latin_name = faculty)
    if not FacultyObj:
        return HttpResponseNotFound('<h1>Такого факультета не существует</h1>')

    GroupObjList = Group.objects.filter(faculty_id = FacultyObj.id)
    all_groups = {}
    urls = {}
    for group in GroupObjList:
        course = group.course
        group_number = group.group_number
        all_groups.setdefault(course, [])
        urls[group_number] = f"/faculties/{faculty}/groups/{group_number}"
        all_groups[course].append({"number" : group_number, "url" : urls[group_number]})
            
    return render(request, 'website/faculty.html', context = { "all_groups" : all_groups })



def groups(request, faculty, group):
    FacultyObj = Faculty.objects.get(latin_name = faculty)
    GroupObj = Group.objects.get(group_number = group)

    # TODO: исправить условие

    if not FacultyObj and not GroupObj:
        return HttpResponseNotFound('<h1>Такой группы не существует</h1>')

    StudentObjList = Student.objects.filter(group = GroupObj.id)
    students = {}

    group_number = Group.objects.get(group_number = group).group_number
    for st in StudentObjList:
        fullname = f"{st.surname} {st.name} {st.patronymic}"
        students[fullname] = f"/faculties/{faculty}/groups/{group}/students/{st.id}"

    return render(request, 'website/group.html', context = {"students" : students,
                                                            "group" : group_number})



def students(request, faculty, group, student_id):
    StudentObj = Student.objects.get(id = student_id)
    fullname_and_group = mu.getFullNameAndGroup(StudentObj)

    #TODO: добавить за весь период

    today = date.today()
    if 'month' in request.GET:
        month = today.month
        year = today.year
        start_date = datetime(year, month, 1)
        end_date = today

    elif 'year' in request.GET:
        year = today.year
        if datetime.today().month < 9:
            year -= 1
        start_date = datetime(year, 9, 1)
        end_date = today

    else:
        iso = datetime.today().isocalendar()
        start_date = datetime.strptime(f'{iso[0]}-{iso[1]-1}-1', '%Y-%W-%w')
        end_date = today
        

    GroupObj = Group.objects.get(group_number = group)
    GroupLessonObjList = Group_Lesson.objects.filter(group = GroupObj)
    LessonObjList = Lesson.objects.filter(id__in = GroupLessonObjList.values("lesson"), date__range = (start_date, end_date))
    attendance = Attendance.objects.filter(student = student_id).values_list("lesson", flat = True)
 
    lessons = []
    for l in LessonObjList:
        status = "Не был"
        # TODO: а где другие статусы из Attendance.status ?
        if l.id in attendance:
            status = "Был"

        lessons.append({"date" : l.date,
                        "name" : l.lesson_name,
                        "aud" : l.auditorium.aud_number,
                        "build" : l.auditorium.building.build_name,
                        "status" : status})

    urls = {"week" : f"{student_id}?week",
            "month" : f"{student_id}?month",
            "year" : f"{student_id}?year"}


    return render(request, 'website/student.html', context = {"lessons" : lessons, 
                                                              "fullname_and_group" : fullname_and_group,
                                                              "urls" : urls})




def buildings(request, building):
    BuildObj = Building.objects.get(latin_name = building)

    if not BuildObj:
        return HttpResponseNotFound('<h1>Такого корпуса не существует</h1>')

    AuditoriumObjList = Auditorium.objects.filter(building_id = BuildObj.id)

    auditoriums = {}

    iso = datetime.today().isocalendar()
    start_date = datetime.strptime(f'{iso[0]}-{iso[1]-1}-1', '%Y-%W-%w')
    end_date = datetime.strptime(f'{iso[0]}-{iso[1]-1}-0', '%Y-%W-%w')
    
    for aud in AuditoriumObjList:
        LessonObjList = Lesson.objects.filter(auditorium_id = aud.id, date__range = (start_date, end_date))
        auditoriums[aud.aud_number] = [None] * (7*6)
        
        for less in LessonObjList:
            auditoriums[aud.aud_number][datetime.weekday(less.date)*7 + less.lesson_number - 1] = {
                                                                "name": less.abbreviation, 
                                                                "url": f"{building}/auditoriums/{aud.aud_number}/date/{less.date}/index/{less.lesson_number}",
                                                                "lesson_name" : less.lesson_name}

    building_name = BuildObj.fullname

    return render(request, 'website/building.html', context = {"auditoriums" : auditoriums,
                                                               "fullname" : building_name})



def lessons(request, building, auditorium, date, index):
    BuildObj = Building.objects.get(latin_name = building)
    AuditoriumObj = Auditorium.objects.get(building_id = BuildObj.id, aud_number = auditorium)
    #TODO: проверить конвертацию даты при запросе у моделей 
    LessonObj = Lesson.objects.get(lesson_number = index, auditorium_id = AuditoriumObj.id, date = date)
    GroupLessonSet = Group_Lesson.objects.filter(lesson_id = LessonObj.id)
    StudentObjList = Student.objects.filter(group__in = GroupLessonSet.values("group"))

    students = []
    for st in StudentObjList:
        attendance = mu.get_if_exists(Attendance, student = st, lesson = LessonObj)
        status = "Не был"
        if attendance is not None:
            status = "Был"
        students.append({"fullname" : mu.getFullName(st),
                         "url_student" : f"/faculties/{st.group.faculty.latin_name}/groups/{st.group.group_number}/students/{st.id}",
                         "url_group" : f"/faculties/{st.group.faculty.latin_name}/groups/{st.group.group_number}",
                         "group" : st.group.group_number,
                         "status" : status})

    #TODO: локализовать дату

    lesson = {"name" : LessonObj.lesson_name,
              "professor" : mu.getFullName(LessonObj.professor),
              "aud" : LessonObj.auditorium.aud_number,
              "build" : LessonObj.auditorium.building.build_name,
              "date" : LessonObj.date}

    return render(request, 'website/lesson.html', context = {"students" : students,
                                                             "lesson" : lesson})
 

class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'website/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # print(mu.isAccauntInProfessorsGroup(user))
            # print(mu.isAccauntInDeaneryGroup(user))
            # print(user.professor.surname)
            # print(user.professor.name)
            # print(user.professor.patronymic)
            return redirect('/')
        else:
            return render(request, 'website/login.html', context={'error_msg': 'Упс... неправильное имя пользователя или пароль'})

def logout(request):
    auth.logout(request)
    return redirect('/')


    