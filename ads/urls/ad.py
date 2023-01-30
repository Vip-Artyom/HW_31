from django.urls import path
from ads.views.ad import AdViewSet, AdImageUpload
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', AdViewSet)

urlpatterns = [
    path("<int:pk>/upload_image/", AdImageUpload.as_view()),
]
urlpatterns += router.urls
