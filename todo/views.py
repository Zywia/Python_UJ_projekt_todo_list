import datetime

from django.contrib.auth.models import User

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from todo.serializer import UserSerializer, TaskSerializer, GroupOfTasksSerializer, FolderSerializer
from todo.models import Task, GroupOfTasks, Folder


class TaskViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['put'])
    def set_done(self, request, pk):
        task = self.get_object()
        task.done = not task.done
        if task.done:
            task.doneDateTime = datetime.datetime.now()
        else:
            task.doneDateTime = None

        task.save()
        return Response({'task': 'done'})

    @action(detail=False)
    def get_all_done(self, request):
        all_tasks = filter(lambda x: x.done, Task.objects.all())
        serializer = self.get_serializer(all_tasks, many=True)
        return Response(serializer.data)

    def get_all_todo(self, request):
        all_tasks = filter(lambda x: not x.done, Task.objects.all())
        serializer = self.get_serializer(all_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def get_all_after_a_deadline(self, request):
        all_tasks = filter(lambda x: datetime.date.today() > x.plannedDate,
                           filter(lambda x: not x.done,
                                  filter(lambda x: x.plannedDate is not None,
                                         Task.objects.all())))
        serializer = self.get_serializer(all_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def get_all_to_do_today(self, request):
        all_tasks = filter(lambda x: datetime.date.today() == x.plannedDate,
                           filter(lambda x: not x.done, Task.objects.all()))
        serializer = self.get_serializer(all_tasks, many=True)
        return Response(serializer.data)

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

    @action(detail=True)
    def get_all_tasks_todo(self, request, pk):
        return self.get_filtered_tasks(False, request)

    @action(detail=True)
    def get_all_tasks_done(self, request, pk):
        return self.get_filtered_tasks(True, request)

    def get_filtered_tasks(self, done: bool, request):
        group = self.get_object()
        tasks = filter(lambda x: x.done is done, group.tasks.all())
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
