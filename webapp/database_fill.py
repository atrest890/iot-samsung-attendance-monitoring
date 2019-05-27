from website.models import *
import re, random, datetime

current_year = 9
def getCourse(group):
    return current_year - int(group[2])


facs = { "РТФ" : ["118", "127", "146-1", "145-2"], 
         "РКФ" : ["218", "227", "246-1", "245-2"], 
         "ФЭТ" : ["318", "327", "346-1", "345-2"], 
         "ФСУ" : ["418", "427", "446-1", "445-2"], 
         "ФВС" : ["518", "527", "546-1", "545-2"],
         "ГФ"  : ["618", "627", "646-1", "645-2"],
         "ЭФ"  : ["818", "827", "846-1", "845-2"],
         "ФИТ" : ["018", "027", "046-1", "045-2"],
         "ЮФ"  : ["098", "097", "096-1", "095-2"],
         "ФБ"  : ["718", "727", "746-1", "745-2"],  }


latin_facs = { "РТФ" : "rtf", 
               "РКФ" : "rkf", 
               "ФЭТ" : "fet", 
               "ФСУ" : "fsu", 
               "ФВС" : "fvs",
               "ГФ"  : "gf",
               "ЭФ"  : "ef",
               "ФИТ" : "fit",
               "ЮФ"  : "yuf",
               "ФБ"  : "fb"  }

builds = { "УЛК" : "ulk",
           "ФЭТ" : "fet",
           "РК"  : "rk",
           "ГК"  : "gk",
           "МК"  : "mk" }


lessons = [ "Теория информации и кодирования",
            "Математическая статистика",
            "Философия",
            "Безопасность операционных систем",
            "Математический анализ",
            "Основы программирования",
            "Языки программирования",
            "Безопасность систем баз данных",
            "Дискретная математика",
            "Иностранный язык",
            "Компьютерное моделирование",
            "Основы криптографии",
            "Технологии и методы программирования",
            "Русский язык",
            "Геометрия",
            "Физика",
            "Информатика",
            "Электроника и схемотехника",
            "Основы ЭВМ и ВС",
            "Теория электрический цепей",
            "История",
            "Алгебра",
            "Менеджмент",
            "Защита интеллектуальной собственности",
            "Проектирование радиосистемы",
            "Космические системы",
            "Правоведение",
            "Безопасность жизнедеятельности",
            "Основы телевидения и радиотехника" ]


auditoriums = []



f = open("names.txt", 'r')
students = f.readlines()
professors = students


for fac, groups in facs.items():
    f, created = Faculty.objects.get_or_create(faculty_name = fac, latin_name = latin_facs[fac])
    print(fac, "created" if created  else "existed")
    for group in groups:
        g, created = Group.objects.get_or_create(group_number = group, faculty = f, course = getCourse(group))
        print("\t", group, "created" if created  else "existed")

for name, latin in builds.items():
    b, created = Building.objects.get_or_create(build_name = name, latin_name = latin)
    print(name, "created" if created  else "existed")


groups_obj = Group.objects.all()
groups = []
for gr in groups_obj:
    groups.append(gr.id)


# for st in students:
#         creds = re.split(" ", st)

#         s, created = Student.objects.get_or_create(surname = creds[0], 
#                                           name = creds[1], 
#                                           patronymic = creds[2],
#                                           group_id = random.choice(groups))


#         print("\t", st, "created" if created  else "existed")


# for pr in professors:
#         creds = re.split(" ", pr)

#         s, created = Professor.objects.get_or_create(surname = creds[0],
#                                                      name = creds[1],
#                                                      patronymic = creds[2])
#         print("\t", pr, "created" if created else "existed")


builds_obj = Building.objects.all()

# for b_obj in builds_obj:
#     for aud in range(200, 230, 1):
#         auditoriums.append(aud) 
#         a, created = Auditorium.objects.get_or_create(aud_number = str(aud), building = b_obj)
#         print("\t", aud, "created" if created else "existed")

#     for aud in range(300, 330, 1):
#         auditoriums.append(aud) 
#         a, created = Auditorium.objects.get_or_create(aud_number = str(aud), building = b_obj)
#         print("\t", aud, "created" if created else "existed")

#     for aud in range(400, 430, 1):
#         auditoriums.append(aud) 
#         a, created = Auditorium.objects.get_or_create(aud_number = str(aud), building = b_obj)
#         print("\t", aud, "created" if created else "existed")


aud_obj = Auditorium.objects.all()
pr_obj = Professor.objects.all()
# for les in lessons:
#         l, created = Lesson.objects.get_or_create(lesson_name = les, 
#                                                 date = datetime.datetime.now(), 
#                                                 lesson_number = random.choice([1, 2, 3, 4, 5, 6, 7]),
#                                                 auditorium = random.choice(aud_obj),
#                                                 professor = random.choice(pr_obj))

#         print("\t", les, "created" if created else "existed")


less_obj = Lesson.objects.all()

for gr in groups_obj:
        gl, created = Group_Lesson.objects.get_or_create(group = gr, lesson = random.choice(less_obj))
        print("\t", "{0} : {1}".format(gl.group.group_number, gl.lesson.lesson_name), "created" if created else "existed")


attendance = Attendance.objects.all()
st_obj = Student.objects.all()


# for i in range(1, 200, 1):
#         a, created = Attendance.objects.get_or_create(student = random.choice(st_obj), lesson = random.choice(less_obj))
#         print("\t", a.student.surname, "created" if created else "existed")
      