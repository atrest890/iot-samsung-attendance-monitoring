from website.models import Student, Group
import django.contrib.auth.models as auth_model

def getFullNameAndGroup(st):
    g = Group.objects.get(id = st.group_id)
    return ("{0} {1} {2} {3}".format(st.surname, st.name, st.patronymic, g.group_number))


def getFullName(obj):
    return ("{0} {1} {2}".format(obj.surname, obj.name, obj.patronymic))

def get_if_exists(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:  # Be explicit about exceptions
        obj = None
    return obj

def getAccauntName(user):
    full = user.get_full_name()
    if full == '':
        return user.username
    return full

def isAccauntInProfessorsGroup(user):
    # TODO: по хорошему надо вынести эти все литералы
    return len(user.groups.filter(name='Преподаватели')) != 0

def isAccauntInDeaneryGroup(user):
    # TODO: по хорошему надо вынести эти все литералы
    return len(user.groups.filter(name='Деканат')) != 0