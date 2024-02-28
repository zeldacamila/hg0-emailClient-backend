from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action

from email_api.serializers import EmailSerializer
from email_api.models import Email


class EmailListViewSet(viewsets.GenericViewSet):
    """
    EmailViewSet class for email operations such as list, create, retrieve, update and delete.
    """

    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path="all")
    def getAllEmails(self, request):
        """
        Method to retrieve all emails.
        Parameters:
            - request: The request object
        Returns:
            - response object with the emails data if the emails are retrieved.
        """

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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path="create")
    def createNewEmail(self, request):
        """
        Method to create a new email.
        Parameters:
            - request: The request object with the email data to be created.
        Returns:
            - Response object with the email data if the email is created successfully.
        """

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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path="sender/<str:sender_email>")
    def getEmailsBySender(self, request, sender_email):
        """
        Method to get all emails by a sender user
        Parameters:
            - request 
            - sender_email: The email of the sender user
        Returns:
            - Response object with the emails data if the emails are retrieved.
        """

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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path="recipient/<str:recipient_email>")
    def getEmailsByRecipient(self, request, recipient_email):
        """
        Method to get all emails by a recipient user
        Parameters:
            - request
            - recipient_email: The email of the recipient user
        Returns:
            - Response object with the emails data if the emails are retrieved.
        """

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

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated], url_path="status/<str:value>")
    def getEmailsByStatus(self, request, value):
        """
        Method to get all emails by status
        Parameters:
            - request
            - value: The status of the email
        Returns:
            - Response object with the emails data if the emails are retrieved.
        """

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


class EmailDetailsViewSet(viewsets.GenericViewSet):
    """
    EmailViewSet class for email operations such as list, create, retrieve, update and delete.
    """

    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated], url_path="update/<int:pk>")
    def updateEmail(self, request, pk):
        """
        Method to update an email.
        Parameters:
            - request: The request object with the email data to be updated.
            - pk: The primary key of the email to be updated.
        Returns:
            - Response object with the email data if the email is updated successfully.
        """
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

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated], url_path="delete/<int:pk>")
    def deleteEmail(self, request, pk):
        """
        Method to delete an email.
        Parameters:
            - request: The request object.
            - pk: The primary key of the email to be deleted.
        Returns:
            - Response object with the email data if the email is deleted successfully.
        """
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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path="get/<int:pk>")
    def getEmail(self, request, pk):
        """
        Method to retrieve an email.
        Parameters:
            - request: The request object.
            - pk: The primary key of the email to be retrieved.
        Returns:
            - Response object with the email data if the email is retrieved successfully.
        """
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


class EmailChangeStatus(APIView):
    """
    EmailChangeStatus class to change the status of an email.
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        """
        Method to change the status of an email.
        Parameters:
            - request: The request object.
            - pk: The primary key of the email to be updated.
        Returns:
            - Response object with the email data if the email status is updated successfully.
        """

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
