from website.models import *

facs = { "РТФ" : ["118", "128", "148-1", "148-2"], 
         "РКФ" : ["218", "228", "248-1", "248-2"], 
         "ФЭТ" : ["318", "328", "348-1", "348-2"], 
         "РТФ" : ["418", "428", "448-1", "448-2"], 
         "ФВС" : ["518", "528", "548-1", "548-2"], 
         "ФБ" : ["718", "728", "748-1", "748-2"]  }

latin_facs = { "РТФ" : "rtf", 
               "РКФ" : "rkf", 
               "ФЭТ" : "fet", 
               "РТФ" : "rtf", 
               "ФВС" : "fvs", 
               "ФБ"  : "fb"  }

builds = { "УЛК" : "ulk",
           "ФЭТ" : "fet",
           "РК"  : "rk",
           "ГК"  : "gk",
           "МК"  : "mk" }


for fac, groups in facs.items():
    f = Faculty(faculty_name = fac, latin_name = latin_facs[fac])
    f.save()

    for group in groups:
        g = Group(group_number = group, faculty = f)
        g.save()

for name, latin in builds.items():
    b = Building(build_name = name, latin_name = latin)
    b.save()