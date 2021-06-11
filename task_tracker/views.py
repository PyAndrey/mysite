from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as user_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from task_tracker.models import Project, Task, User
from task_tracker.forms import CustomUserCreationForm, ProjectForm, TaskForm
# Create your views here.


def index(request):
    """Главная страница"""
    return render(request, 'base.html')


def login(request):
    """Страница авторизации"""
    if request.method != 'POST':
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            authenticated_user = authenticate(
                username=user.username, password=request.POST['password'])
            user_login(request, authenticated_user)
            return HttpResponseRedirect(reverse('task_tracker:account', args=[user.id]))
    context = {'form': form}
    return render(request, 'task_tracker/login.html', context)


def logout_view(request):
    """Переадресация на главную, после выхода пользователя"""
    logout(request)
    return HttpResponseRedirect(reverse('task_tracker:index'))


def register(request):
    """Страница регистрации"""
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user.username)
            authenticated_user = authenticate(
                username=new_user.username, password=request.POST['password1'])
            user_login(request, authenticated_user)
            return HttpResponseRedirect(reverse('task_tracker:account', args=[new_user.id]))
    context = {'form': form}
    return render(request, 'task_tracker/register.html', context)


def account(request, id):
    """Фильтр постов по id пользователя"""
    projects = Project.objects.filter(user=id)
    return render(request, 'task_tracker/account.html', context={'projects': projects})


def project_tasks(request, project_id):
    """Фильтр задач к конкретным проектам"""
    try:
        if request.GET.get('task_status'):
            tasks = Task.objects.filter(
                project=project_id, status=request.GET['task_status'])
        elif request.GET.get('task_name'):
            tasks = Task.objects.filter(
                project=project_id, task_name=request.GET['task_name'])
        else:
            tasks = Task.objects.filter(project=project_id)
            print(tasks)
    except:
        raise Http404('Задачи не найдены')

    return render(request, 'task_tracker/project_tasks.html', context={'project': tasks, 'project_id': project_id})


def create_project(request, user_id):
    """Страница создания проекта"""
    error = ''
    try:
        user = User.objects.get(id=user_id)

    except:
        raise Http404('Пользователь не найден')
    if request.method != 'POST':
        form = ProjectForm()
    else:
        form = ProjectForm(request.POST)
        if form.is_valid():

            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return HttpResponseRedirect(reverse('task_tracker:account', args=(user.id,)))
        else:
            error = 'Форма была неверной'

    context = {'form': form, 'error': error, 'user': user}
    return render(request, 'task_tracker/create_project.html', context)


def create_task(request, project_id):
    """Страница создания задачи"""
    error = ''
    try:
        project = Project.objects.get(id=project_id)
    except:
        raise Http404('Проект не найден')
    if request.method != 'POST':
        form = TaskForm()
        print(project)
    else:
        form = TaskForm(request.POST)
        if form.is_valid():

            entry = form.save(commit=False)
            entry.project = project
            entry.save()
            return HttpResponseRedirect(reverse('task_tracker:project_tasks', args=(project.id,)))
        else:
            error = 'Форма была неверной'

    context = {'form': form, 'error': error, 'project': project}
    return render(request, 'task_tracker/create_task.html', context)


def edit_task(request, project_id, task_id):
    """Страница редактирования задачи"""
    try:
        project = Project.objects.get(id=project_id)
        task = Task.objects.get(id=task_id)
    except:
        raise Http404('Проект не найден')
    if request.method == 'POST':
        task.task_name = request.POST.get("task_name")
        task.task_text = request.POST.get("task_text")
        task.save()

        return HttpResponseRedirect(reverse('task_tracker:project_tasks', args=(project.id,)))

    context = {'project': project, 'task': task}
    return render(request, 'task_tracker/edit_task.html', context)
