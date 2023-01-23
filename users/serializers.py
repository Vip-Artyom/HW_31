from rest_framework import serializers
from users.models import Users, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True)

    class Meta:
        model = Users
        fields = ['username', 'location']


class UserListSerializer(serializers.ModelSerializer):
    total_ads = serializers.IntegerField()

    class Meta:
        model = Users
        exclude = ['password', 'location']


class UserSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True)

    class Meta:
        model = Users
        exclude = ['password']


class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, many=True,
                                            slug_field="name", queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_user = Users.objects.create(**validated_data)
        for loc in self._locations:
            loc, created = Location.objects.get_or_create(name=loc)
            new_user.location.add(loc)
        return new_user

    class Meta:
        model = Users
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False, many=True,
                                            slug_field="name", queryset=Location.objects.all())

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("location", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.location.all().delete()
        for loc in self._locations:
            loc, created = Location.objects.get_or_create(name=loc)
            user.location.add(loc)
        return user

    class Meta:
        model = Users
        fields = "__all__"
