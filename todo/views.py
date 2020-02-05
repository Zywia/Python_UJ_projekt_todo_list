from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from todo.serializer import UserSerializer, TaskSerializer, GroupOfTasksSerializer, FolderSerializer
from todo.models import Task, GroupOfTasks, Folder


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GroupOfTasksViewSet(viewsets.ModelViewSet):
    queryset = GroupOfTasks.objects.all()
    serializer_class = GroupOfTasksSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
