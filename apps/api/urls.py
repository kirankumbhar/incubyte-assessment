from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.views import ItemViewSet

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
]
