from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    pass


    # def __str__(self):
    #     return self.article_title

    # def was_published_recently(self):
    #     return self.pub_date >= (timezone.now() - datetime.timedelta(days=7))

    # class Meta:
    #     verbose_name = 'Статья'
    #     verbose_name_plural = 'Статьи'


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField('название проекта', max_length=50)
    project_text = models.CharField('описание проекта', max_length=200)
    create_date = models.DateTimeField('дата создания проекта', auto_now_add=True)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Status(models.TextChoices):
    WAITING = 'WT', 'Ожидание'
    IMPLEMENTATION = 'IM', 'Реализация'
    TESTING = 'TE', 'Проверка'
    RELEASE = 'RE', 'Выпуск'


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.CharField('Название задачи', max_length=50)
    task_text = models.CharField('описание задачи', max_length=200)
    create_date = models.DateTimeField('дата создания задачи', auto_now_add=True)
    status = models.CharField(
        'статус задачи',
        max_length=2,
        choices=Status.choices,
        default=Status.WAITING,
    )
    def __str__(self):
        return f"{self.task_name} - {Status(self.status).label}"

    def get_status_display(self):
        return Status(self.status).label

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
