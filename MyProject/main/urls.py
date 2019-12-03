from django.urls import path
from main.views.ViewSets import OrderViewSet, ReviewViewSet
from rest_framework import routers
# from core.views import ProjectListAPIView


# urlpatterns = [
#     path('projects/', ProjectListAPIView.as_view())
# ]

router = routers.DefaultRouter()
router.register('reviews', ReviewViewSet, base_name='main')
router.register('orders', OrderViewSet, base_name='main')


urlpatterns = router.urls