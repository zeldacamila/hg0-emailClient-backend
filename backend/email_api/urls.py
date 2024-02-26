from rest_framework.urls import path
import email_api.views as views

urlpatterns = [
    path("list/", views.EmailList.as_view(), name="email-list"),
    path("list/sender/<str:sender_email>/",
         views.EmailListBySender.as_view(), name="email-list-sender"),
    path("list/recipient/<str:recipient_email>/",
         views.EmailListByRecipient.as_view(), name="email-list-recipient"),
    path("list/status/<str:value>/",
         views.EmaiListByStatus.as_view(), name="email-list-status"),
    path("detail/<int:pk>/", views.EmailDetail.as_view(), name="email-details"),
    path("status/read/<int:pk>/", views.EmailChangeStatus.as_view(),
         name="email-change-status"),
]
