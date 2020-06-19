from django.shortcuts import redirect


def student_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.account.is_student:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper_func


def teacher_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.account.is_teacher:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper_func
