from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Account, Student, Teacher, Classes, Classroom
from .decorators import student_required, teacher_required
from django.http import HttpResponse


def registerPage(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        status = request.POST.get('status')
        if form.is_valid():
            c_user = form.save()
            username = form.cleaned_data.get('username')
            if status == "student":
                Student.objects.create(
                    user=c_user,
                    name=c_user.username,
                    is_student=True,
                )
            elif status == "teacher":
                Teacher.objects.create(
                    user=c_user,
                    name=c_user.username,
                    is_teacher=True,
                )
            messages.success(request, f'Account created for {username}! You can now login')
            return redirect('login')
    else:
        form = CreateUserForm()
    context = {
        'form': form,
    }
    return render(request,'users/register.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or password incorrect')
    context = {}
    return render(request, 'users/login.html', context)


def logoutPage(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    current_user = request.user.account
    if current_user.is_student:
        class1 = Classroom.objects.filter(student__name=current_user)
        students = None
        try:
            percent = round((current_user.student.correct / current_user.student.attempt) * 100, 2)
        except ZeroDivisionError:
            percent = 0
    elif current_user.is_teacher:
        class1 = current_user.teacher.classes_set.all()
        students = Classroom.objects.filter(classes__name='Stoichiometry Basics')
        percent = 0
    context = {
        'c_user': current_user,
        'percent': percent,
        'class': class1,
        'students': students,
    }
    return render(request, 'users/dashboard.html', context)


@login_required(login_url='login')
@student_required
def purchase(request):
    current_user = request.user.account
    if request.method == "POST":
        time = int(request.POST.get('time'))
        current_user.student.balance += time
        current_user.student.save()
        return redirect('dashboard')
    context = {
        'c_user': current_user,
    }
    return render(request, 'users/purchase.html', context)


@login_required(login_url='login')
def view_class(request):
    user = request.user.account
    classes = Classes.objects.all()
    context = {
        'classes': classes,
        'c_user': user,
    }
    return render(request, 'users/view_class.html', context)


@login_required(login_url='login')
def signup(request, pk):
    c_user=request.user.account
    class_name = Classes.objects.get(id=pk)
    this_class = Classroom.objects.filter(classes__name=class_name)
    existing = this_class.filter(student__name=c_user).exists()

    if request.method == "POST":
        if not existing:
            Classroom.objects.create(
                classes=class_name,
                student=c_user.student,
            )
            messages.success(request, f'You have signed up for {class_name}')
            return redirect('view-class')
        elif existing:
            messages.warning(request, f"You have already signed up for {class_name}")
            return redirect('view-class')
    context = {
        'class': class_name
    }
    return render(request, 'users/signup.html', context)


@login_required(login_url='login')
@student_required
def leave_class(request,pk):
    c_user = request.user.account
    class_name = Classroom.objects.get(id=pk)
    this_class = Classroom.objects.filter(classes__name=class_name)
    class_slot = this_class.get(student__name=c_user)
    if request.method == "POST":
        class_slot.delete()
        messages.success(request, "You have left the class")
        return redirect('dashboard')
    context = {'class': class_name}
    return render(request, 'users/leave_class.html', context)


@login_required(login_url='login')
@teacher_required
def add_class(request):
    user = request.user.account
    if request.method == "POST":
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        print("123", name, cost, capacity, description)
        Classes.objects.create(
            name=name,
            capacity=capacity,
            cost=cost,
            description=description,
            teacher=user.teacher
        )
        return redirect('view-class')
    return render(request, 'users/add_class.html')