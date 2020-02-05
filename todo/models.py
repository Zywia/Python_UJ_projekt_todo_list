from django.db import models


# Create your models here.

class Folder(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['title']


class GroupOfTasks(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    parentFolder = models.ForeignKey('Folder', related_name='folders',
                                     on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['title']


class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    dateOfPlannedRealization = models.DateTimeField(null=True, blank=True)
    dateOfActualRealization = models.DateTimeField(null=True, blank=True)

    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField()
    parentGroupOfTasks = models.ForeignKey('GroupOfTasks', related_name='tasks', on_delete=models.CASCADE)

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

