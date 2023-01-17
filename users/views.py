import json

from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView
from users.models import Users, Location


class UserDetailView(DetailView):
    model = Users

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": [loc.name for loc in user.location.all()],
        }, safe=False)


class UserListView(ListView):
    model = Users
    queryset = Users.objects.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse(
            [{
                "id": user.pk,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "total_ads": user.total_ads,
                "locations": [loc.name for loc in user.location.all()]
                } for user in self.object_list], safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = Users
    fields = "__all__"

    def post(self, request, **kwargs):
        data = json.loads(request.body)

        user = Users.objects.create(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("username"),
            role=data.get("role"),
            age=data.get("age"),
            password=data.get("password"),
        )
        locations = data.get("locations")

        if locations:
            for loc_name in data.get("locations"):
                loc, created = Location.objects.get_or_create(name=loc_name)
                user.location.add(loc)

        return JsonResponse({
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": [loc.name for loc in user.location.all()],
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = Users
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if "first_name" in data:
            self.object.first_name = data.get("first_name")
        if "last_name" in data:
            self.object.last_name = data.get("last_name")
        if "username" in data:
            self.object.username = data.get("username")
        if "role" in data:
            self.object.role = data.get("role")
        if "age" in data:
            self.object.age = data.get("age")
        if "locations" in data:
            self.object.location.all().delete()
            for loc_name in data.get("locations"):
                loc, created = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)

        return JsonResponse({
            "id": self.object.pk,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [loc.name for loc in self.object.location.all()],
        }, safe=False)

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.first_name = data.get("first_name")
        self.object.last_name = data.get("last_name")
        self.object.username = data.get("username")
        self.object.role = data.get("role")
        self.object.age = data.get("age")

        self.object.location.all().delete()
        for loc_name in data.get("locations"):
            loc, created = Location.objects.get_or_create(name=loc_name)
            self.object.location.add(loc)

        return JsonResponse({
            "id": self.object.pk,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [loc.name for loc in self.object.location.all()],
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = Users
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": user.id}, safe=False)
