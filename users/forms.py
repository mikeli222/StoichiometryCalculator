from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm


class CreateUserForm(UserCreationForm):
    CHOICES = [('student', 'Student'), ('teacher', 'Teacher')]
    status = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'status']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'