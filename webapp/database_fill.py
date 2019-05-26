from website.models import *
import re, random

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


f = open("names.txt", 'r')
students = f.readlines()


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


for st in students:
        creds = re.split(" ", st)

        s, created = Student.objects.get_or_create(surname = creds[0], 
                                          name = creds[1], 
                                          patronymic = creds[2],
                                          group_id = random.choice(groups))


        print("\t", st, "created" if created  else "existed")


