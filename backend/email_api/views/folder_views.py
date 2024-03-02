from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from email_api.models import Folder
from email_api.serializers import FolderSerializer

class FolderViewSet(viewsets.ModelViewSet):

    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]
    queryset = Folder.objects.all()
    
    def list(self, request):
        """
        Method to get all folders.
        """
        folders = Folder.objects.filter(user=request.user)
        serializer = self.get_serializer(folders, many=True)
        return Response({
            "data": serializer.data,
            "status": status.HTTP_200_OK,
            "success": True
        }, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Method to create a folder.
        """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Folder created successfully",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED,
                "success": True
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Invalid data",
            "data": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Method to delete a folder.
        """
        folder = Folder.objects.filter(id=pk, user=request.user).first()
        if folder:
            folder.delete()
            return Response({
                "message": "Folder deleted successfully",
                "status": status.HTTP_204_NO_CONTENT,
                "success": True
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            "message": "Folder does not exist",
            "status": status.HTTP_404_NOT_FOUND,
            "success": False
        }, status=status.HTTP_404_NOT_FOUND)
