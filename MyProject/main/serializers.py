from .models import City,ReviewedCompany,AudCompany,Auditor,Order,Person,Review
from rest_framework import serializers
from users.serializers import UserSerializer

from users.serializers import UserSerializer



class AudCompanySerializer(serializer.ModelSerializer):
    class Meta:
        model = AudCompany
        fields = '__all__'


class ReviewedCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewedCompany
        fields = '__all__'


class OrderShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'name', 'company_id')


class OrderSerializer(OrderShortSerializer):

    class Meta(OrderShortSerializer.Meta):
        fields = OrderShortSerializer.Meta.fields + ('created_at')


class ReviewShortSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField()
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('title', 'status', 'auditor_id','company_id', 'order_id', 'created_at','created_by')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''


class ReviewFullSerializer(serializers.ModelSerializer):
    class Meta(ReviewShortSerilalizer):
        fields = ReviewShortSerilalizer.Meta.fields + ('description', 'body')

class ReviewSerializer(ReviewShortSerializer):
    pass


class AuditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditor
        fields = '__all__'







