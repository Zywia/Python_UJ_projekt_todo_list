from enum import IntEnum

from django.db import models


# Create your models here.

class Folder(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=1000, blank=True, default='')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']


class GroupOfTasks(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=1000, default='')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    folder = models.ForeignKey('Folder', related_name='groups',
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']


class Task(models.Model):
    class PriorityLevels(IntEnum):
        Minor = 1
        Normal = 2
        Major = 3
        Critical = 4

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    title = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=1000, blank=True, default='')
    groupOfTasks = models.ForeignKey('GroupOfTasks', related_name='tasks', on_delete=models.CASCADE)
    task_priority = models.IntegerField(choices=PriorityLevels.choices(), default=PriorityLevels.Normal)
    doneDateTime = models.DateTimeField(blank=True, null=True)
    plannedDate = models.DateField(blank=True, null=True)
    done = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']
