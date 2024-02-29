from rest_framework.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

import email_api.views as views

# urlpatterns for email operations
urlpatterns = [
    path("status/read/<int:pk>", views.EmailChangeStatus.as_view(),
         name="email-change-status"),
    path("list/all",
         views.EmailListViewSet.as_view({"get": "getAllEmails"}), name="email-list"),
    path("list/create", views.EmailListViewSet.as_view(
        {"post": "createNewEmail"}), name="email-create"),
    path("list/sender/<str:sender_email>",
         views.EmailListViewSet.as_view({"get": "getEmailsBySender"}), name="email-sender"),
    path("list/recipient/<str:recipient_email>", views.EmailListViewSet.as_view(
        {"get": "getEmailsByRecipient"}), name="email-recipient"),
    path("list/status/<str:value>",
         views.EmailListViewSet.as_view({"get": "getEmailsByStatus"}), name="email-status"),
    path("detail/<int:pk>",
         views.EmailDetailsViewSet.as_view({"get": "getEmail", "put": "updateEmail", "delete": "deleteEmail"}), name="email-detail"),
]
