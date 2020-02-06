from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from todo.models import Folder, GroupOfTasks, Task
from todo.serializer import FolderSerializer, GroupOfTasksSerializer, TaskSerializer
from todo.views import TaskViewSet


class AbstractTestClass(APITestCase):
    def startTests(self, model_name) -> None:
        self.user = User.objects.create(username='zywia', password='nieistotne')
        self.client.force_authenticate(self.user)
        factory = APIRequestFactory()
        request = factory.get('/')
        self.objectString = model_name
        self.serializer_context = {
            'request': Request(request),
        }


class TestFolderViewSet(AbstractTestClass):
    def setUp(self) -> None:
        self.startTests('folder')
        self.shop = Folder.objects.create(title='shop', owner=self.user)
        self.project = Folder.objects.create(title='project', owner=self.user)
        self.studies = Folder.objects.create(title='studies', owner=self.user)

    def test_get_all_folders(self):
        response = self.client.get(reverse('folder-list'))
        folders = Folder.objects.all()
        serializer = FolderSerializer(folders, many=True, context=self.serializer_context)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_folder(self):
        response = self.client.get(
            reverse('folder-detail', kwargs={'pk': self.shop.pk}))
        folder = Folder.objects.get(pk=self.shop.pk)
        serializer = FolderSerializer(folder, context=self.serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_folder(self):
        response = self.client.get(
            reverse('folder-detail', kwargs={'pk': 109000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestGroupOfTasksViewSet(AbstractTestClass):

    def setUp(self) -> None:
        self.startTests('groupoftasks')
        self.shop = GroupOfTasks.objects.create(title='shop', owner=self.user)
        self.project = GroupOfTasks.objects.create(title='project', owner=self.user)
        self.studies = GroupOfTasks.objects.create(title='studies', owner=self.user)

    def test_get_all_groupOfTasks(self):
        response = self.client.get(reverse(self.objectString + '-list'))
        group_of_tasks = GroupOfTasks.objects.all()
        serializer = GroupOfTasksSerializer(group_of_tasks, many=True, context=self.serializer_context)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_groupOfTask(self):
        response = self.client.get(
            reverse(self.objectString + '-detail', kwargs={'pk': self.shop.pk}))
        group_of_task = GroupOfTasks.objects.get(pk=self.shop.pk)
        serializer = GroupOfTasksSerializer(group_of_task, context=self.serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_groupOfTask(self):
        response = self.client.get(
            reverse(self.objectString + '-detail', kwargs={'pk': 109000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestTaskViewSet(AbstractTestClass):
    def setUp(self) -> None:
        self.startTests('task')
        self.task_view_set = TaskViewSet(**self.serializer_context)
        self.shop = Task.objects.create(title='shop', owner=self.user)
        self.project = Task.objects.create(title='project', owner=self.user)
        self.studies = Task.objects.create(title='studies', owner=self.user)

    def test_get_all_groupOfTasks(self):
        response = self.client.get(reverse(self.objectString + '-list'))
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True, context=self.serializer_context)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_groupOfTask(self):
        response = self.client.get(
            reverse(self.objectString + '-detail', kwargs={'pk': self.shop.pk}))
        tasks = Task.objects.get(pk=self.shop.pk)
        serializer = TaskSerializer(tasks, context=self.serializer_context)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_groupOfTask(self):
        response = self.client.get(
            reverse(self.objectString + '-detail', kwargs={'pk': 109000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


