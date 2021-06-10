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
    path('accounts/<int:user_id>/create_project/', views.create_project, name='create_project'),
]
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<int:article_id>/', views.detail, name='detail'),
#     path('<int:article_id>/leave_comment/', views.leave_comment, name='leave_comment'),
# ]
