from django.db import models
import django.contrib.auth.models as auth_model

class Building(models.Model):
    build_name = models.CharField(max_length = 10, unique = True)
    fullname = models.CharField(max_length = 40, unique = True, default = "")
    latin_name = models.CharField(max_length = 10, unique = True, default = "")


class Auditorium(models.Model):
    aud_number = models.CharField(max_length = 10)
    building = models.ForeignKey(Building, on_delete = models.CASCADE)


class Faculty(models.Model):
    faculty_name = models.CharField(max_length = 5, unique = True)
    latin_name = models.CharField(max_length = 5, unique = True, default = "")
    short_name = models.CharField(max_length = 40, unique = True)


class Group(models.Model):
    group_number = models.CharField(max_length = 10, unique = True)
    faculty = models.ForeignKey(Faculty, on_delete = models.CASCADE)
    course = models.IntegerField(default = 0)


 
class Student(models.Model):
    surname = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    patronymic = models.CharField(max_length = 50)
    group = models.ForeignKey(Group, on_delete = models.CASCADE, default = "")
    identifier = models.CharField(max_length = 32, unique = True, default = "0de8ddf24fd4424e2a0d29a21de4880e")


class Professor(models.Model):
    # TODO: разобраться с именами в моделях, ибо в user уже есть поля first_name и last_name
    surname = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    patronymic = models.CharField(max_length = 50)
    account = models.OneToOneField(auth_model.User, on_delete=models.CASCADE)

# TODO: мб стоит наследовать User?
class Deanery(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete = models.CASCADE)
    account = models.OneToOneField(auth_model.User, on_delete=models.CASCADE)

class Lesson(models.Model):
    lesson_name = models.CharField(max_length = 40)
    abbreviation = models.CharField(max_length = 20, default = "")
    date = models.DateField()
    lesson_number = models.IntegerField()
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, on_delete = models.CASCADE)


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE)
    status = models.CharField(max_length = 10, default = "Был")


class Group_Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE)


