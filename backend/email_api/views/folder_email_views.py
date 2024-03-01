from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from email_api.models import Folder, FolderEmail, Email

from email_api.serializers import FolderEmailSerializer, EmailSerializer

class FolderEmailViewSet(viewsets.ModelViewSet):
    
    serializer_class = FolderEmailSerializer
    permission_classes = [IsAuthenticated]
    queryset = FolderEmail.objects.all()

    @action(detail=False, methods=['get'])
    def get_emails_by_folder(self, request, folder_id):
        """
        Method to get all emails in a folder.
        """

        try:
            user = request.user
            folder = Folder.objects.get(id=folder_id, user=user)
            folder_emails = FolderEmail.objects.filter(folder=folder)
            email_ids = folder_emails.values_list("email_id", flat=True)
            emails = Email.objects.filter(id__in=email_ids)
            serializer = EmailSerializer(emails, many=True)
            return Response({
                "data": serializer.data,
                "status": status.HTTP_200_OK,
                "success": True
            }, status=status.HTTP_200_OK)
        except Folder.DoesNotExist:
            return Response({
                "data": "Folder does not exist",
                "status": status.HTTP_404_NOT_FOUND,
                "success": False
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "data": str(e),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def add_email_to_folder(self, request):
        """
        Method to add an email to a folder.
        """
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success": True
            }, status=status.HTTP_201_CREATED)
        return Response({
            "data": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'])
    def remove_email_from_folder(self, request, email_id=None, folder_id=None):
        """
        Method to remove an email from a folder.
        """
        try:
            user = request.user
            folder = Folder.objects.get(id=folder_id, user=user)
            folder_email = FolderEmail.objects.get(folder=folder, email_id=email_id)
            folder_email.delete()
            return Response({
                "message": "Email removed from folder",
                "status": status.HTTP_204_NO_CONTENT,
                "success": True
            }, status=status.HTTP_204_NO_CONTENT)
        except Folder.DoesNotExist:
            return Response({
                "message": "Folder does not exist",
                "status": status.HTTP_404_NOT_FOUND,
                "success": False
            }, status=status.HTTP_404_NOT_FOUND)
        except FolderEmail.DoesNotExist:
            return Response({
                "message": "Email does not exist in folder",
                "status": status.HTTP_404_NOT_FOUND,
                "success": False
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "message": str(e),
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







        
