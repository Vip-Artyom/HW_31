from ads.views.cat import CatViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', CatViewSet)

urlpatterns = [
]

urlpatterns += router.urls
