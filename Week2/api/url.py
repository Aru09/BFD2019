from django.urls import path
# from api.views import ProjectListViewSet, ProjectViewSet
from rest_framework import routers
from api.views import ProjectListAPIView, ProjectDetailAPIView, TaskViewSet, BlockListAPIView, MemberProjectViewSet, TaskCommentViewSet, TaskDocumentViewSet


urlpatterns = [
    path('projects/', ProjectListAPIView.as_view(), name='project_list'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view()),
    path('blocks/', BlockListAPIView.as_view()),
]

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet, base_name='api')
router.register('member_projects', MemberProjectViewSet, base_name='api')
router.register('task_documents', TaskDocumentViewSet, base_name='api')
router.register('task_comments', TaskCommentViewSet, base_name='api')


urlpatterns = router.urls