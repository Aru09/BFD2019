from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Review, City, AudCompany,ReviewedCompany
from main.serializers import AudCompanySerializer,ReviewedCompanySerializer,OrderSerializer, AuditorSerializer
from django.http import Http404
from rest_framework import generics
from rest_framework import mixins
from main.models import Order, Auditor

class AudCompanyListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        audcompany = AudCompany.objects.all()
        serializer = AudCompanySerializer(audcompany, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AudCompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class AudCompanyDetail(APIView):

    def get_object(self, pk):
        try:
            return AudCompany.objects.get(pk=pk)
        except AudCompany.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        audcompany = self.get_object(pk)
        serializer = AudCompanySerializer(audcompany)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        audcompany = self.get_object(pk)
        serializer = AudCompanySerializer(audcompany, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        audcompany = self.get_object(pk)
        audcompany.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewedCompanyListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        revcompany = ReviewedCompany.objects.all()
        serializer = ReviewedCompanySerializer(revcompany, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewedCompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class AuditorDetailAPIView(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    queryset = Auditor.objects.all()
    serializer_class = AuditorSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



