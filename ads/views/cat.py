from rest_framework.viewsets import ModelViewSet
from ads.serializers.cat_serializers import *


class CatViewSet(ModelViewSet):
    queryset = Category.objects.order_by('name')
    default_serializer = CatSerializer

    def get_serializer_class(self):
        return self.default_serializer
