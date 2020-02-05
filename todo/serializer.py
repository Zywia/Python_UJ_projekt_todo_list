from django.contrib.auth.models import User
from rest_framework import serializers


from todo.models import GroupOfTasks, Task, Folder


class GroupOfTasksSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    tasks = serializers.HyperlinkedRelatedField(many=True, view_name='task-detail', read_only=True)

    class Meta:
        model = GroupOfTasks
        fields = '__all__'


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = '__all__'


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    groupOfTasks = serializers.HyperlinkedRelatedField(many=True, view_name='groupOfTasks-detail', read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # tasks = serializers.HyperlinkedRelatedField(many=True, view_name='task-detail', read_only=True)
    groups = serializers.HyperlinkedRelatedField(many=True, view_name='groupOfTasks-detail', read_only=True)
    # folders = serializers.HyperlinkedRelatedField(many=True, view_name='folder-detail', read_only=True)

    class Meta:
        model = User
        fields =  [ 'groups']
