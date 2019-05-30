from website.models import Student, Group



def getFullNameAndGroup(st):
    g = Group.objects.get(id = st.group_id)
    return ("{0} {1} {2} {3}".format(st.surname, st.name, st.patronymic, g.group_number))


def getFullName(st):
    return ("{0} {1} {2}".format(st.surname, st.name, st.patronymic))

def get_if_exists(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:  # Be explicit about exceptions
        obj = None
    return obj