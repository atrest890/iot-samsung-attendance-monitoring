from django.db import models
 
class Student(models.Model):
    surname = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    patronymic = models.CharField(max_length = 50)


class Professor(models.Model):
    surname = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    patronymic = models.CharField(max_length = 50)


class Building(models.Model):
    build_name = models.CharField(max_length = 10)


class Auditorium(models.Model):
    aud_number = models.CharField(max_length = 10)
    building = models.ForeignKey(Building, on_delete = models.CASCADE)

    

class Group(models.Model):
    number = models.CharField(max_length = 10)
    group_number = models.CharField(max_length = 10)

class Faculty(models.Model):
    faculty_name = models.CharField(max_length = 5)


class Lesson(models.Model):
    lesson_name = models.CharField(max_length = 20)
    date = models.DateField()
    lesson_number = models.IntegerField()
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, on_delete = models.CASCADE)


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE)


class Group_Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete = models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete = models.CASCADE)


