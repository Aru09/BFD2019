from rest_framework import serializers
from api.models import Block, Project, Task, TaskComment, TaskDocument,MemberProject
from api.utils import constants
from users.serializers import UserSerializer

class TaskSerializer2(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    creator = serializers.CharField(source='creator.username')
    description = serializers.CharField()


    class Meta:
        model = TaskDocument
        fields = ('id', 'name', 'description', 'creator')


class TaskDocumentSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(write_only=True)
    creator = UserSerializer(read_only=True)
    task = TaskSerializer2(read_only=True)

    class Meta:
        model = TaskDocument
        fields = '__all__'

class TaskCommentSerializer(serializers.ModelSerializer):
    task_id = serializers.IntegerField(write_only=True)
    creator = UserSerializer(read_only=True)
    task = TaskSerializer2(read_only=True)

    class Meta:
        model = TaskComment
        fields = '__all__'

class TaskShortSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'status', 'project_id', 'creator')


class TaskFullSerializer(TaskShortSerializer):
    class Meta(TaskShortSerializer.Meta):
        fields = TaskShortSerializer.Meta.fields + ('description',)

class TaskSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(write_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'status', 'project_id', 'creator', 'description')





class BlockSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Block
        fields = ('id', 'name', 'type', 'type_name', 'project_id', 'project_name', 'created_at')

    def get_project_name(self, obj):
        if obj.project is not None:
            return obj.project.name
        return ''

    def get_type_name(self, obj):
        d = dict(constants.BLOCK_TYPES)
        return d[int(obj.type)]

class ProjectSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'creator_id', 'creator_name', 'created_at')


    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''




class ProjectSerializer2(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name= serializers.CharField(required=True)
    creator= serializers.CharField(source='creator.username')
    description = serializers.CharField()
    tasks= TaskSerializer2(many=True, read_only=True, required=False)
    blocks= BlockSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Project
        fields = ('id', 'name', 'creator', 'description', 'tasks')



class MemberProjectSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(write_only=True)
    project_id = serializers.IntegerField(write_only=True)
    member = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = MemberProject
        fields = '__all__'




