from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ads.models import Selection
from users.models import UserRoles, Users


class SelectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", queryset=Users.objects.all(), required=False)

    def create(self, validated_data):
        request = self.context.get('request')
        if "owner" not in validated_data:
            validated_data["owner"] = request.user
        elif "owner" in validated_data and request.user.role == UserRoles.MEMBER and \
                request.user != validated_data["owner"]:
            return ValidationError("Нет доступа")
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'
