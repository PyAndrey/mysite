from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as user_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from task_tracker.models import Project, Task, User
from task_tracker.forms import CustomUserCreationForm, ProjectForm, TaskForm
from django.utils import timezone
# Create your views here.


def index(request):
    return render(request, 'base.html')


def login(request):
    if request.method != 'POST':
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            authenticated_user = authenticate(username=user.username, password=request.POST['password'])
            user_login(request, authenticated_user)
            return HttpResponseRedirect(reverse('task_tracker:account', args=[user.id]))
    context={'form': form}
    return render(request, 'task_tracker/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('task_tracker:index'))


def register(request):
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
    # Фильтр постов по id пользователя
    projects = Project.objects.filter(user=id)
    return render(request, 'task_tracker/account.html', context={'projects':projects})


# def index(request):
#     latest_articles_list = Article.objects.order_by('-pub_date')[:5]
#     return render(request, 'articles/list.html', {'latest_articles_list': latest_articles_list})


def project_tasks(request, project_id):
    try:
        if request.GET.get('task_status'):
            tasks = Task.objects.filter(project=project_id, status=request.GET['task_status'])
        elif request.GET.get('task_name'):
            tasks = Task.objects.filter(project=project_id, task_name=request.GET['task_name'])
        else:
            tasks = Task.objects.filter(project=project_id)
            print(tasks)
    except:
        raise Http404('Задачи не найдены')

    # task_filter_list = Task.objects.filter(status=)
    # a.comment_set.order_by(-id)[:10]
    # return render(request, 'articles/detail.html', {'article': a, 'latest_comments_list': latest_comments_list})
    return render(request, 'task_tracker/project_tasks.html', context={'project':tasks, 'project_id': project_id})


def create_project(request, user_id):
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
            return HttpResponseRedirect(reverse('task_tracker:account', args = (user.id,)))
        else:
            error = 'Форма была неверной'

    context={'form': form, 'error': error, 'user': user}
    return render(request, 'task_tracker/create_project.html', context)

    
def create_task(request, project_id):
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
            
            # entry = form.save()
            entry = form.save(commit=False)
            entry.project = project
            entry.save()
            return HttpResponseRedirect(reverse('task_tracker:project_tasks', args = (project.id,)))
        else:
            error = 'Форма была неверной'

    context={'form': form, 'error': error, 'project': project}
    return render(request, 'task_tracker/create_task.html', context)
    

# Task.objects.filter(status='WT')

# def leave_comment(request, article_id):
#     try:
#         a = Article.objects.get(id=article_id)
#     except:
#         raise Http404('Статья не найдена')
#     a.comment_set.create(author_name = request.POST['name'], comment_text = request.POST['text'])
#     return HttpResponseRedirect(reverse('articles:detail', args = (a.id,)))
