from django.shortcuts import render
from django.http import HttpResponseNotFound
from website.models import Student, Faculty, Auditorium, Building, Group, Group_Lesson, Lesson, Professor, Attendance
import cyrtranslit
import website.model_utils as mu
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

    return render(request, 'website/header.html', context = {"faculties" : faculties, 
                                                             "buildings" : buildings})



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
            
    print(urls)
    return render(request, 'website/faculty.html', context = { "all_groups" : all_groups })



def groups(request, faculty, group):
    FacultyObj = Faculty.objects.get(latin_name = faculty)
    GroupObj = Group.objects.get(group_number = group)

    # TODO: исправить условие

    if not FacultyObj and not GroupObj:
        return HttpResponseNotFound('<h1>Такой группы не существует</h1>')

    StudentObjList = Student.objects.filter(group = GroupObj.id)
    students = {}

    for st in StudentObjList:
        fullname = f"{st.surname} {st.name} {st.patronymic}"
        students[fullname] = f"/faculties/{faculty}/groups/{group}/students/{st.id}"

    return render(request, 'website/group.html', context = {"students" : students})



def students(request, faculty, group, student_id):
    # # FacultyObj = Faculty.objects.get(latin_name = kwargs['faculty'])
    # # GroupObj = Group.objects.get(group_number = kwargs['group'])
    # StudentObj = Student.objects.get(id = student_id)
    #   # TODO: исправить условие

    # if not StudentObj:
    #     return HttpResponseNotFound('<h1>Такого студента не существует</h1>')

    # GroupObj = Group.objects.get(group_number = group)   
    # GroupObjList = Group_Lesson.objects.filter(group_id = GroupObj.id)

    # LessonObjList = []
    # for gl in GroupObjList:
    #     LessonObj = Lesson.objects.get(id = gl.lesson_id)
    #     LessonObjList.append(LessonObj)


    # AttendanceObjList = Attendance.objects.all()
    # current_attendance = []
    # for a in AttendanceObjList:
    #     current_attendance.append(a.student_id)

    
    # lessons = []
    # general_attendance = []

    # for gn in GroupObjList:
    #     general_attendance.append(gn.group_id)

    # # TODO: исправить посещение по группам

    # for less in LessonObjList:
    #     lesson = []
    #     for i in range(1, 5, 1):
    #         lesson.append(less.date)

    #         lesson.append(less.lesson_name)
            
    #         aud = Auditorium.objects.get(id = less.auditorium_id)
    #         lesson.append(aud.aud_number)

    #         build = Building.objects.get(id = aud.building_id)
    #         lesson.append(build.build_name)

    #         student_in_group = Student.objects.get(id = student_id)

    #         if student_in_group.group_id in general_attendance and less.id in current_attendance:
    #             lesson.append("Был")
    #         elif student_in_group.group_id in general_attendance and less.id not in current_attendance:
    #             lesson.append("Не был")
            

            
    #     lessons.append(lesson)

    # fullname_and_group = mu.getFullNameAndGroup(StudentObj)

    # return render(request, 'website/student.html', context = {"lessons" : lessons, 
    #                                                           "fullname_and_group" : fullname_and_group})

    GroupObj = Group.objects.get(group_number = group)
    GroupLessonObjList = Group_Lesson.objects.filter(group = GroupObj)
    LessonObjList = Lesson.objects.filter(id__in = GroupLessonObjList.values("lesson"))

    # attendance = Attendance.objects.filter(student = student_id)
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
    
    return render(request, 'website/student.html', context = {"lessons" : lessons})



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
            auditoriums[aud.aud_number][datetime.weekday(less.date)*7 + less.lesson_number - 1] = {"name": less.lesson_name, 
                                                               "url": f"{building}/auditoriums/{aud.aud_number}/date/{less.date}/index/{less.lesson_number}"}


    return render(request, 'website/building.html', context = {"auditoriums" : auditoriums})



def lessons(request, building, auditorium, date, index):
    # if kwargs['building'] == 'ulk':
    #     if kwargs['auditorium'] == '403':
    #         if kwargs['date'] == '2019.05.05':
    #             if kwargs['index'] == 1:
    #                 return render(request, 'website/attendance_all.html')
    # return HttpResponseNotFound('<h1>Такой пары не существует</h1>')

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

    return render(request, 'website/lesson.html', context = {"students" : students})





        