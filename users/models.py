from django.db import models
from django.contrib.auth.models import User
from django.apps import apps


# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class Student(Account):
    balance = models.IntegerField(default=0, null=True)
    correct = models.IntegerField(default=0, null=True)
    attempt = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.name


class Teacher(Account):
    earning = models.FloatField(default=0, null=True)

    def __str__(self):
        return self.name


class Classes(models.Model):
    name = models.CharField(max_length=100, null=True)
    capacity = models.IntegerField(null=True, default=1)
    cost = models.IntegerField(null=True, default=0)
    description = models.CharField(null=True, max_length=500)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    classes = models.ForeignKey(Classes, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.classes.name

