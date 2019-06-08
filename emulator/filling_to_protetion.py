
# python3 manage.py shell -c "exec(open('../emulator/filling_to_protetion.py').read())"


try:
    from website.models import *
    from datagate.models import *
    from integration.models import *
except:
    from webapp.website.models import *
    from webapp.datagate.models import *
    from webapp.integration.models import *

import datetime

def getId(num):
    import hashlib
    return hashlib.md5(num.to_bytes(4, 'big')).hexdigest()

# 707
aud, created = Auditorium.objects.get_or_create(aud_number = '707', building = Building.objects.get(build_name='УЛК'))
print(aud, "created" if created else "existed")
ID = 'f2e50d503396c297d13284d7849c9846'
dev, created = Device.objects.get_or_create(identifier=ID, auditorium = aud)
print(dev, "created" if created else "existed")

# test fac
f, created = Faculty.objects.get_or_create(faculty_name = 'TEST', latin_name = 'TEST')
print(f, "created" if created else "existed")

# 111-t
g1, created = Group.objects.get_or_create(group_number = '111-t', faculty = f, course = 1)
print('\t', g1, "created" if created else "existed")

# test user 1 2375558084
s, created = Student.objects.get_or_create(surname = 'test', name = 'user1', identifier = getId(2375558084), group = g1)
print('\t\t', s, "created" if created else "existed")
# test user 2 566502340
s, created = Student.objects.get_or_create(surname = 'test', name = 'user2', patronymic='22222', identifier = getId(566502340), group = g1)
print('\t\t', s, "created" if created else "existed")

# 236-t
g2, created = Group.objects.get_or_create(group_number = '236-t', faculty = f, course = 2)
print('\t', g2, "created" if created else "existed")

# test user 3 1017717700
s, created = Student.objects.get_or_create(surname = 'test', name = 'user3', patronymic='333333', identifier = getId(1017717700), group = g2)
print('\t\t', s, "created" if created else "existed")
# test user 4 3317834692
s, created = Student.objects.get_or_create(surname = 'test', name = 'user3', identifier = getId(3317834692), group = g2)
print('\t\t', s, "created" if created else "existed")

professor_gr, cr = auth_model.Group.objects.get_or_create(name='Преподаватели')
decan_gr, cr = auth_model.Group.objects.get_or_create(name='Деканат')
account, created = auth_model.User.objects.get_or_create(first_name='iot', last_name='sumsung', username='iot_sumsung')
account.set_password('1234')
account.groups.add(decan_gr)
account.groups.add(professor_gr)
account.save()
print(account, "created" if created else "existed")

p, created = Professor.objects.get_or_create(surname = 'iot', name = 'tusur', patronymic = 'sumsung', account=account)
print(p, "created" if created else "existed")

d, created = Deanery.objects.get_or_create(faculty=f, account=account)
print(d, "created" if created else "existed")

for i in range(1, 6):
        # засчищаем место для защиты
        Lesson.objects.filter(date = datetime.datetime(2019, 6, 8), lesson_number = i, auditorium = aud).delete()

        less, created = Lesson.objects.get_or_create(abbreviation='IOT', lesson_name = 'IOT', date = datetime.datetime(2019, 6, 8, 13, 15), lesson_number = i, auditorium = aud, professor = p)
        print(less, "created" if created else "existed")

        gl, created = Group_Lesson.objects.get_or_create(group = g1, lesson = less)
        print('\t', gl, "created" if created else "existed")
        gl, created = Group_Lesson.objects.get_or_create(group = g2, lesson = less)
        print('\t', gl, "created" if created else "existed")

