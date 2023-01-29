from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ads.models import Selection
from ads.permissions import IsSelectionOwner
from ads.serializers.selection import SelectionSerializer


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer

    default_permission_classes = [AllowAny(), ]
    permissions_list = {"create": [IsAuthenticated()],
                        "update": [IsAuthenticated(), IsSelectionOwner()],
                        "partial_update": [IsAuthenticated(), IsSelectionOwner()],
                        "destroy": [IsAuthenticated(), IsSelectionOwner()],
                        }

    def get_permissions(self):
        return self.permissions_list.get(self.action, self.default_permission_classes)
