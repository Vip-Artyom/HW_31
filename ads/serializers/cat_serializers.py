from rest_framework import serializers
from ads.models import Category


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
