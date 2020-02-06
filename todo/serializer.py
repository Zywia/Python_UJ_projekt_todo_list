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
        read_only_fields = ['doneDateTime', 'done', 'created']


class FolderSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    groups = serializers.HyperlinkedRelatedField(many=True, view_name='groupoftasks-detail',
                                                 read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    task_set = serializers.HyperlinkedRelatedField(many=True, view_name='task-detail',
                                                   read_only=True)
    groupoftasks_set = serializers.HyperlinkedRelatedField(many=True,
                                                           view_name='groupoftasks-detail',
                                                           read_only=True)
    folder_set = serializers.HyperlinkedRelatedField(many=True, view_name='folder-detail',
                                                     read_only=True)

    class Meta:
        model = User
        fields = '__all__'
