from website.models import Student, Group



def getFullNameAndGroup(st):
    g = Group.objects.get(id = st.group_id)
    return ("{0} {1} {2} {3}".format(st.surname, st.name, st.patronymic, g.group_number))



