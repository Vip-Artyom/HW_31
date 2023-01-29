from rest_framework.permissions import BasePermission


class IsSelectionOwner(BasePermission):
    message = "Вы не имеете прав изменять эту подборку"

    def has_object_permission(self, request, view, selection):
        if request.user == selection.owner:
            return True
        return False
