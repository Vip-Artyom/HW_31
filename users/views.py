from django.db.models import Count, Q
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from users.serializers import *
from users.models import Users


class UserPagination(PageNumberPagination):
    page_size = 2


class LocationViewSet(ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = Users.objects.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True))).order_by("username")
    pagination_class = UserPagination


class UserDetailView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = Users.objects.all()


class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = Users.objects.all()


class UserDeleteView(DestroyAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()
