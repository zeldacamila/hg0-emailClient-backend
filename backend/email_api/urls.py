from rest_framework.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

import email_api.views as views

# router for email operations
router = DefaultRouter()
router.register("list", views.EmailListViewSet, basename="")
router.register("detail", views.EmailDetailsViewSet, basename="")

# urlpatterns for email operations
urlpatterns = [
    path("status/read/<int:pk>/", views.EmailChangeStatus.as_view(),
         name="email-change-status"),
    path("", include(router.urls))
]
