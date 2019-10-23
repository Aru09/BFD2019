from rest_framework import viewsets, mixins, status, generics
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as status_codes

from django.http import Http404
from django.shortcuts import get_object_or_404
from users.serializers import MainUser
from api.models import Project, Task, Block, TaskComment, TaskDocument, MemberProject
from api.serializers import ProjectSerializer, BlockSerializer, TaskShortSerializer, TaskFullSerializer,ProjectSerializer2 ,TaskCommentSerializer, TaskDocumentSerializer, MemberProjectSerializer

from api.constants import TODO




class BlockListAPIView(APIView):
    http_method_names = ['get', 'post']

    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        blocks = Block.objects.all()
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ProjectListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data)
        return Response(serializer.data)

class ProjectDetailAPIView(APIView):
    http_method_names = ['get', 'put', 'delete']

    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(data=project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer2(instance=project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)



class TaskViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskFullSerializer
        if self.action == 'set_executor':
            pass
        return TaskShortSerializer

    @action(methods=['PUT'], detail=True)
    def set_executor(self, request, pk):
        # request.data
        return Response('executor updated')


class TaskDocumentViewSet(viewsets.ModelViewSet):
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

class MemberProjectViewSet(viewsets.ModelViewSet):
    queryset = MemberProject.objects.all()
    serializer_class = MemberProjectSerializer

    def perform_create(self, serializer):
        member = get_object_or_404(MainUser, pk=self.request.data['member_id'])
        project = get_object_or_404(Project, pk=self.request.data['project_id'])
        if serializer.is_valid():
            serializer.save(member=member, project=project)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        member = get_object_or_404(MainUser, pk=self.request.data['member_id'])
        project = get_object_or_404(Project, pk=self.request.data['project_id'])
        if serializer.is_valid():
            serializer.save(member=member, project=project)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)
