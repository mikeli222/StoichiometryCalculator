from django.contrib import admin
from .models import Account, Student, Teacher, Classes, Classroom

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Classes)
admin.site.register(Classroom)