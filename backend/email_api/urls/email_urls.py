from rest_framework.urls import path

from email_api.views import EmailChangeStatus, EmailListViewSet, EmailDetailsViewSet, FolderEmailViewSet

# urlpatterns for email operations
urlpatterns = [
    path("status/read/<int:pk>/", EmailChangeStatus.as_view(),
         name="email-change-status"),
    path("list/all/?<str:subject>/",
         EmailListViewSet.as_view({"get": "getAllEmails"}), name="email-list"),
    path("list/create/", EmailListViewSet.as_view(
        {"post": "createNewEmail"}), name="email-create"),
    path("list/sender/<str:sender_email>/",
         EmailListViewSet.as_view({"get": "getEmailsBySender"}), name="email-sender"),
    path("list/recipient/<str:recipient_email>/", EmailListViewSet.as_view(
        {"get": "getEmailsByRecipient"}), name="email-recipient"),
    path("list/status/<str:value>/",
         EmailListViewSet.as_view({"get": "getEmailsByStatus"}), name="email-status"),
    path("detail/<int:pk>/",
         EmailDetailsViewSet.as_view({"get": "getEmail", "put": "updateEmail", "delete": "deleteEmail"}), name="email-detail"),
    path("folders/<int:folder_id>/", FolderEmailViewSet.as_view({"get": "get_emails_by_folder"}), name="email-folder"),
    path("folders/", FolderEmailViewSet.as_view(
        {"post": "add_email_to_folder"}), name="email-folder-add"),
    path("<int:email_id>/folders/<int:pk>/", FolderEmailViewSet.as_view(
        {"delete": "remove_email_from_folder"}), name="email-folder-remove"),
]
