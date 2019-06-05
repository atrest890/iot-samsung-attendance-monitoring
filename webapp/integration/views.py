from django.views import View
from django.http import HttpResponse

import website.models as wm
import requests as r
import random
import hashlib
from enum import Enum
from datetime import datetime, timedelta
from lxml import html, etree
from traceback import print_exc

class Periods(Enum):
    BEFORE_BREAKING = 0
    AFTER_BREAKING = 1
    EXAM_SESSION = 2
    UNKNOWN = 3

class Integration(View):

    def get(self, request):
        try:

            self.__tusur()

            return HttpResponse('done')
        except Exception:
            print("Integration ERROR!")
            print_exc()
            return HttpResponse('error')

    def __tusurExcaptionOnNot200(self, ans):
        if ans.status_code != 200:
            raise Exception(f'TUSUR site responce {ans.status_code} code on {ans.url}')

    def __tusur(self):

        self.__tusurParseInit()

        # TODO: подумать как получать за другие недели

        # получаем факультеты
        facs = self.__tusurFaculty()
        # получаем список групп
        for f in facs:
            f['groups'] = self.__tusurGroups(f['original_url'])

        # получаем корпуса
        buildings = self.__tusurBuilding()
        # получаем пары и преподов
        professors = {}
        for b in buildings:
            b['lessons'] = self.__tusurLessons(b['original_url'], self._currweek_id)
            for less in b['lessons']:
                # TODO: а преподов так то может быть несколько...
                surname, name, patronymic = self.__tusurSplitProfessor(less['professor'])
                professors[less['professor']] = {
                    'name' : name,
                    'surname' : surname,
                    'patronymic' : patronymic
                }

        print("All professors:")
        print(professors)

        # =(

        print("\n\nFilling database...\n\n")
        print('Faculty...')
        for fac in facs:
            f, cr = wm.Faculty.objects.get_or_create(faculty_name=fac['faculty_name'], latin_name=fac['latin_name'])
            print(f.faculty_name, 'created' if cr else 'existed')
            for course, groups in enumerate(fac['groups'], start=1):
                print(f'\tCourse {course}...')
                for group in groups:
                    g, cr = wm.Group.objects.get_or_create(group_number=group['group_number'], course=course, faculty=f)
                    print('\t\t', g.group_number, 'created' if cr else 'existed')
                    print('\t\t\tStudent:')
                    for i in range(random.randint(5, 15)):
                        surname, name, patronymic, identifier = self.__tusurGenStudent(f.latin_name, g.group_number, i)
                        s, cr = wm.Student.objects.get_or_create(surname=surname, name=name, patronymic=patronymic, identifier=identifier, group=g)
                        print(f'\t\t\t{i}:', s.surname, s.name, s.patronymic, s.identifier, 'created' if cr else 'existed')

        print('Professors...')
        for fullname, prof in professors.items():
            p, cr = wm.Professor.objects.get_or_create(surname=prof['surname'], name=prof['name'], patronymic=prof['patronymic'])
            prof['obj'] = p
            print(fullname, 'created' if cr else 'existed')


        print('Building...')
        for building in buildings:
            b, cr = wm.Building.objects.get_or_create(build_name=building['build_name'], latin_name=building['latin_name'])
            print(b.build_name, 'created' if cr else 'existed')
            print('\tAuditoriums...')
            for aud in building['audiences']:
                a, cr = wm.Auditorium.objects.get_or_create(aud_number=aud, building=b)
                print('\t', a.aud_number, 'created' if cr else 'existed')
            print('\tLessons...')
            for less in building['lessons']:
                auditorium = wm.Auditorium.objects.get(aud_number=less['auditorium'], building=b)
                l_obj, cr = wm.Lesson.objects.get_or_create(lesson_name=less['lesson_name'], 
                                                            date=less['date'], 
                                                            lesson_number=less['lesson_number'], 
                                                            professor=professors[less['professor']]['obj'],
                                                            auditorium=auditorium)
                print('\t', l_obj.lesson_name, 'created' if cr else 'existed')
                print('\t\tGroup lessons...')
                for group in less['groups']:
                    g = wm.Group.objects.get(group_number=group)
                    _, cr = wm.Group_Lesson.objects.get_or_create(group=g, lesson=l_obj)
                    print('\t\t', group, '-', l_obj.lesson_name, 'created' if cr else 'existed')


    def __tusurParseInit(self):
        """
        Стадия инициализации метоинфы для парсинга расписания
        """
        ans = r.get('https://timetable.tusur.ru/')
        self.__tusurExcaptionOnNot200(ans)

        page = html.fromstring(ans.content)
        periods_a = page.xpath('.//ul[@class="current_timetable_info"]/li/a')

        self._currentPeriod = Periods.UNKNOWN
        periods = [i.attrib['href'] for i in periods_a]
        
        # TODO: это пока нигде не применятеся, возможно надо вместо енама ввести префикс
        if '/before_breaking' not in periods:
            self._currentPeriod = Periods.BEFORE_BREAKING
        elif '/after_breaking' not in periods:
            self._currentPeriod = Periods.AFTER_BREAKING
        elif '/exam_session' not in periods:
            self._currentPeriod = Periods.EXAM_SESSION

        if self._currentPeriod == Periods.EXAM_SESSION:
            raise Exception('Exam session dont support yet')

        # TODO: не всегда есть этот виджет
        ans = r.get('https://timetable.tusur.ru/buildings/mk')
        self.__tusurExcaptionOnNot200(ans)

        page = html.fromstring(ans.content)
        self._currweek_id = int(page.xpath('.//li[@class="tile current"]/a')[0].attrib['href'].split('=')[-1])

        iso = datetime.today().isocalendar()
        self._currweek_date = datetime.strptime(f'{iso[0]}-{iso[1]-1}-1', '%Y-%W-%w')

    def __tusurSplitProfessor(self, fullname):
        # Surname N.P.
        # Surname1 N1.P1., Surname2 N2.P2.
        parts = fullname.split(' ')
        
        if len(parts) == 2 and parts[1].count('.') == 2:
            return (parts[0], parts[1][0:2], parts[1][2:])
        else:
            return (fullname, "", "")

    def __tusurGenStudent(self, faculty, group, idx):
        surname = f"surname_{group}_{idx}"
        name = f"name_{faculty}_{idx}"
        patr = f"p_{faculty}_{group}"

        return (surname, name, patr, hashlib.md5((surname+name+patr).encode()).hexdigest())

    def __tusurGetBeginDateByWeekId(self, week_id):
        dw = self._currweek_id - week_id

        iso = self._currweek_date.isocalendar()
        # TODO: может быть отрицательная неделя, тогда надо декрементировать год
        return datetime.strptime(f'{iso[0]}-{iso[1]-1-dw}-1', '%Y-%W-%w')


    def __tusurGetWeekIdByDate(self, date):
        # TODO: пора бы уже вынести это в utils
        iso = date.isocalendar()        
        target = datetime.strptime(f'{iso[0]}-{iso[1]-1}-1', '%Y-%W-%w')

        dw = ((self._currweek_date - target) // 7).days

        return self._currweek_id - dw

    def __tusurGetTimeLessonByNumber(self, num):
        if num == 1:
            return timedelta(hours=8, minutes=50)
        elif num == 2:
            return timedelta(hours=10, minutes=40)
        elif num == 3:
            return timedelta(hours=13, minutes=15)
        elif num == 4:
            return timedelta(hours=15, minutes=00)
        elif num == 5:
            return timedelta(hours=16, minutes=45)
        elif num == 6:
            return timedelta(hours=18, minutes=30)
        elif num == 7:
            return timedelta(hours=20, minutes=15)
        else:
            raise Exception('Supported only 7 lesson')

    def __tusurFaculty(self):
        """
        Возвращает список факультетов, представленные словарём из latin_name, faculty_name и original_url
        """
        ans = r.get('https://timetable.tusur.ru/')
        self.__tusurExcaptionOnNot200(ans)

        page = html.fromstring(ans.content)
        facs = page.xpath('.//ul[@class="faculties"]/li')

        res = []

        for f in facs:
            a = f.xpath('.//a')[0]
            res.append({
                'latin_name' : f.attrib['class'],
                'faculty_name' : a.text,
                'original_url' : a.attrib['href']
            })
            print('Faculty found:', res[-1])

        return res

    def __tusurGroups(self, faculty_url):
        """
        Возвращает список курсов, которые являются списоком групр, представленные словарём из group_number и original_url
        """
        ans = r.get('https://timetable.tusur.ru' + faculty_url)
        self.__tusurExcaptionOnNot200(ans)

        page = html.fromstring(ans.content)
        courses = page.xpath('.//div[@class="col-md-12 faculty"]/ul')

        res = []

        for course in courses:
            res_course = []
            for group in course:
                a = group[0]
                res_course.append({
                    'group_number' : a.text,
                    'original_url' : a.attrib['href']
                })
                print('Group found:', res_course[-1])
            res.append(res_course)

        return res

    def __tusurBuilding(self):
        """
            Возвращает список корпусов и аудиторий, представленные build_name, latin_name, original_url и списком аудиторий
        """

        ans = r.get('https://timetable.tusur.ru')
        self.__tusurExcaptionOnNot200(ans)

        page = html.fromstring(ans.content)
        buildings = page.xpath('.//div[@class="building_charging"]/ul/li/a')

        res = []

        for a in buildings:
            name, auds = self.__tusurAuditory(a.attrib['href'])
            res.append({
                'original_url' : a.attrib['href'],
                'latin_name' : a.attrib['href'].split('/')[-1],
                'build_name' : name,
                'audiences' : auds
            })
            print('Building found:', res[-1])

        return res

    def __tusurAuditory(self, building_url):
        """
            Возвращает тупл из имени корпуса и списка аудиторий
        """

        ans = r.get('https://timetable.tusur.ru' + building_url)
        self.__tusurExcaptionOnNot200(ans)

        page = html.fromstring(ans.content)
        buiding_name = page.xpath('.//h1')[0].text.split(',')[0]

        auds = page.xpath('.//span[@class="auditorium_info"]/a')

        res = []

        for a in auds:
            res.append(a.text)

        return (buiding_name, res)

    def __tusurLessons(self, building_url, week_id):
        """
            Вовзращает список пар, представленные lesson_name, date, lesson_number, auditorium, professor и groups, представленные списоком
        """

        # TODO: ломка и сессия
        ans = r.get('https://timetable.tusur.ru' + building_url + '?week_id=' + str(week_id))
        self.__tusurExcaptionOnNot200(ans)

        page = html.fromstring(ans.content)
        lessons = page.xpath('.//span[@class="media auditorium-tooltip"]')

        res = []

        for less in lessons:
            td = less.getparent()
            # print('DEBUG', len(td.xpath('.//div/p')))

            tooltip = td.xpath('.//div/p')
            name_p, group_p, prof_p = tooltip[0], tooltip[1], tooltip[2]

            tr = td.getparent()
            auditorium = tr.xpath('.//span[@class="auditorium_info"]/a')[0].text

            idx = tr.index(td)
            number = (idx % 7) + 1
            dd = idx // 7

            date = self.__tusurGetBeginDateByWeekId(week_id)
            date += timedelta(days = dd) + self.__tusurGetTimeLessonByNumber(number)

            if prof_p.text == None or prof_p.text.strip() == "":
                prof = "Without professor"
            else:
                prof = prof_p.text

            res.append({
                'lesson_name' : name_p.text,
                'auditorium' : auditorium,
                'groups' : group_p.text.split(', '),
                'professor' : prof,
                'date' : date,
                'lesson_number' : number
            })
            print('Lesson found:', res[-1])

        return res
