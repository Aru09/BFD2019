import logging
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from main.models import Order, Review
from main.serializers import OrderSerializer, ReviewShortSerializer, ReviewFullSerializer, ReviewSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404


from main.constants import ORDER_WAITING


logger = logging.getLogger(__name__)


class OrderListViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(creator=self.request.user)

    @action(methods=['GET'], detail=False)
    def my(self, request):
        orders = Order.objects.filter(creator=self.request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def s(self, request, pk):
        instance = self.get_object()
        serializer = OrderSerializer(instance.orders, many=True)
        return Response(serializer.data)


class ReviewViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewShortSerializer
        if self.action == 'retrieve':
            return ReviewFullSerializer
        if self.action in ['create', 'update']:
            return ReviewSerializer

    @action(methods=['PUT'], detail=True)
    def set_auditor(self, request, pk):
        instance = self.get_object()
        instance.set_executor(request.data.get('auditor_id'))
        serializer = self.get_serializer(instance)
        logger.info(f"{self.request.user} set as auditor id: {request.data.get('auditor_id')}")
        return Response(serializer.data)

