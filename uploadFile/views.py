from uploadFile.models import File
from rest_framework.views import APIView 
from rest_framework import generics
from .serializers import FileSerializer
from rest_framework.response import Response
from rest_framework import status
import os


""" this part is for the uploading file """

class FileView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    

# class FileView(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         queryset = File.objects.all()
#         serializer_class = FileSerializer
#         serializer = FileSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def post(request):
#         serializer = FileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    
