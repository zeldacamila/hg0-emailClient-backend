from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from email_api.serializers import EmailSerializer
from email_api.models import Email
from user_api.models import User


class EmailList(APIView):
    """
    List all emails, or create a new email.
    """

    def get(self, request):
        emails = Email.objects.all()
        serializer = EmailSerializer(emails, many=True)
        return Response(
            {
                "message": "Emails retrieved successfully",
                "data": serializer.data,
                "success": True,
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = EmailSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Email sent successfully",
                    "data": serializer.data,
                    "success": True,
                    "status": status.HTTP_201_CREATED
                }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "message": serializer.errors,
                    "success": False,
                    "data": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST
            )


class EmailDetail(APIView):
    """
    Retrieve, update or delete an email instance.
    """

    def get(self, request, pk):
        try:
            email = Email.objects.get(pk=pk)
            serializer = EmailSerializer(email)
            return Response(
                {
                    "message": "Email retrieved successfully",
                    "data": serializer.data,
                    "success": True,
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )
        except Email.DoesNotExist:
            return Response(
                {
                    "message": "Email does not exist",
                    "success": False,
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            email = Email.objects.get(pk=pk)
            serializer = EmailSerializer(email, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Email updated successfully",
                        "data": serializer.data,
                        "success": True,
                        "status": status.HTTP_200_OK
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": serializer.errors,
                        "success": False,
                        "data": serializer.errors,
                        "status": status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        except Email.DoesNotExist:
            return Response(
                {
                    "message": "Email does not exist",
                    "success": False,
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, pk):
        try:
            email = Email.objects.get(pk=pk)
            email.delete()
            return Response(
                {
                    "message": "Email deleted successfully",
                    "success": True,
                    "status": status.HTTP_204_NO_CONTENT
                }, status=status.HTTP_204_NO_CONTENT
            )
        except Email.DoesNotExist:
            return Response(
                {
                    "message": "Email does not exist",
                    "success": False,
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND
            )


class EmailListBySender(APIView):
    """
    List emails sent by a specific sender.
    """

    def get(self, request, sender_email):
        emails = Email.objects.filter(sender__email=sender_email)
        serializer = EmailSerializer(emails, many=True)
        return Response(
            {
                "message": f"Emails sent by {sender_email} retrieved successfully",
                "data": serializer.data,
                "success": True,
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )


class EmailListByRecipient(APIView):
    """
    List emails received by a specific recipient.
    """

    def get(self, request, recipient_email):
        emails = Email.objects.filter(recipient__email=recipient_email)
        serializer = EmailSerializer(emails, many=True)
        return Response(
            {
                "message": f"Emails received by {recipient_email} retrieved successfully",
                "data": serializer.data,
                "success": True,
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK
        )


class EmaiListByStatus(APIView):

    def get(self, request, value):
        if value == "true":
            emails = Email.objects.filter(status=True)
            serializer = EmailSerializer(emails, many=True)
            return Response(
                {
                    "message": "Emails readed by retrieved successfully",
                    "data": serializer.data,
                    "success": True,
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )
        else:
            emails = Email.objects.filter(status=False)
            serializer = EmailSerializer(emails, many=True)
            return Response(
                {
                    "message": "Emails unreaded retrieved successfully",
                    "data": serializer.data,
                    "success": True,
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )


class EmailChangeStatus(APIView):

    def put(self, request, pk):
        try:
            email = Email.objects.get(pk=pk)
            email.status = True
            email.save()
            serializer = EmailSerializer(email)
            return Response(
                {
                    "message": "Email read status changed successfully",
                    "data": serializer.data,
                    "success": True,
                    "status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK
            )
        except Email.DoesNotExist:
            return Response(
                {
                    "message": "Email does not exist",
                    "success": False,
                    "status": status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND
            )
