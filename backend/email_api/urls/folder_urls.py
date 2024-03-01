from django.urls import path
from rest_framework.routers import DefaultRouter
from email_api.views.folder_views import FolderViewSet

router = DefaultRouter()
router.register(r"", FolderViewSet, basename="folder")
urlpatterns = router.urls

