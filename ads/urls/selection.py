from rest_framework.routers import SimpleRouter
from ads.views.selection import SelectionViewSet

router = SimpleRouter()
router.register('', SelectionViewSet)

urlpatterns = [
]

urlpatterns += router.urls
