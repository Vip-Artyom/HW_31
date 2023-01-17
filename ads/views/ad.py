import json
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView
from ads.models import Ad, Category
from users.models import Users

PAGE_NUMBER = 2


def root(request):
    return JsonResponse({"status": "ok"})


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": f"{ad.author.first_name} {ad.author.last_name}",
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category.name,
        }, safe=False)


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.all().select_related("author")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, PAGE_NUMBER)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        return JsonResponse(
            {"total": page_object.paginator.count,
             "num_pages": page_object.paginator.num_pages,
             "items": [{"id": ad.id,
                        "name": ad.name,
                        "author_id": ad.author_id,
                        "author": ad.author.first_name,
                        "price": ad.price,
                        "description": ad.description,
                        "is_published": ad.is_published,
                        "category_id": ad.category_id,
                        "image": ad.image.url if ad.image else None} for ad in page_object]}
        )
    
    
@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = "__all__"

    def post(self, request, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(Users, username=data["username"])
        category = get_object_or_404(Category, name=data["category"])

        ad = Ad.objects.create(
            name=data["name"],
            author=author,
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"],
            category=category,
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "category": ad.category.name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
        }, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = "__all__"

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.author = get_object_or_404(Users, username=data["username"])
        self.object.category = get_object_or_404(Category, name=data["category"])
        self.object.price = data["price"]
        self.object.is_published = data["is_published"]
        self.object.description = data["description"]
        self.object.name = data["name"]
        
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "category": self.object.category.name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published}, safe=False)

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if "author" in data:
            self.object.author = get_object_or_404(Users, username=data["username"])
        if "category" in data:
            self.object.category = get_object_or_404(Category, name=data["category"])
        if "price" in data:
            self.object.price = data["price"]
        if "is_published" in data:
            self.object.is_published = data["is_published"]
        if "description" in data:
            self.object.description = data["description"]
        if "name" in data:
            self.object.name = data["name"]

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "category": self.object.category.name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published}, safe=False)
    

@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        ad = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({"id": ad.id}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdImageUpload(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()
        return JsonResponse({"name": self.object.name, "image": self.object.image.url})
