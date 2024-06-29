from rest_framework.serializers import ModelSerializer
from base.models import GeneralReviews

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = GeneralReviews
        fields = '__all__'