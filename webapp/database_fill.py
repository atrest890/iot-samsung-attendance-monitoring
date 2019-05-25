from website.models import *

current_year = 9
def getCourse(group):
    return current_year - int(group[2])


facs = { "РТФ" : ["118", "128", "148-1", "148-2"], 
         "РКФ" : ["218", "228", "248-1", "248-2"], 
         "ФЭТ" : ["318", "328", "348-1", "348-2"], 
         "ФСУ" : ["418", "428", "448-1", "448-2"], 
         "ФВС" : ["518", "528", "548-1", "548-2"],
         "ГФ"  : ["618", "628", "648-1", "648-2"],
         "ЭФ"  : ["818", "828", "848-1", "848-2"],
         "ФИТ" : ["018", "028", "048-1", "048-2"],
         "ЮФ"  : ["098", "098", "098-1", "098-2"],
         "ФБ"  : ["718", "728", "748-1", "748-2"],  }


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



for fac, groups in facs.items():
    f, created = Faculty.objects.get_or_create(faculty_name = fac, latin_name = latin_facs[fac])
    print(fac, "created" if created  else "existed")
    for group in groups:
        g, created = Group.objects.get_or_create(group_number = group, faculty = f, course = getCourse(group))
        print("\t", group, "created" if created  else "existed")

for name, latin in builds.items():
    b, created = Building.objects.get_or_create(build_name = name, latin_name = latin)
    print(name, "created" if created  else "existed")


