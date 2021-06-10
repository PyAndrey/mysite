from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Project
from django.forms.widgets import TextInput, Textarea
from django.utils import timezone
from task_tracker.models import Task

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'password')


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('user', 'project_name', 'project_text')
        exclude = ( 'user',)
        widgets = {
            "project_name": TextInput(
                attrs={
                    'placeholder': 'Название'
                }
            ),
            "project_text": Textarea(
                attrs={
                    'placeholder': 'Текст'
                }
            )
        }


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('project', 'task_name', 'task_text')
        exclude = ( 'project',)
        widgets = {
            "task_name": TextInput(
                attrs={
                    'placeholder': 'Название'
                }
            ),
            "task_text": Textarea(
                attrs={
                    'placeholder': 'Текст'
                }
            )
        }