from django.urls import path
from . import views

app_name = 'task_tracker'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout_view, name='logout_view'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/<int:id>/', views.account, name='account'),
    path('accounts/project/<int:project_id>/', views.project_tasks, name='project_tasks'),
    path('accounts/project/<int:project_id>/create_task/', views.create_task, name='create_task'),
    path('accounts/project/<int:project_id>/edit_task/<int:task_id>', views.edit_task, name='edit_task'),
    path('accounts/<int:user_id>/create_project/', views.create_project, name='create_project'),
]
