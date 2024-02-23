from rest_framework.urls import path

from email_api.views import EmailList, EmailListBySender, EmailListByRecipient, EmailDetail

urlpatterns = [
    path("list/", EmailList.as_view(), name="email-list"),
    path("list/sender/<str:sender_email>/",
         EmailListBySender.as_view(), name="email-list-sender"),
    path("list/recipient/<str:recipient_email>/",
         EmailListByRecipient.as_view(), name="email-list-recipient"),
    path("detail/<int:pk>/", EmailDetail.as_view(), name="email-details"),
]
