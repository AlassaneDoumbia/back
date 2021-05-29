# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import Group, User
from rest_framework import viewsets
from rest_framework import permissions
from testapi.serializers import GroupSerializer
from django.utils.translation import ugettext_lazy as _
from django_currentuser.middleware import get_current_authenticated_user
from rest_framework.decorators import action, api_view 



from django.contrib.auth.hashers import make_password
from django.db.models import Q

@api_view(['GET'])
def ping(request):
    """
    List all code snippets, or create a new snippet.
    """
    return Response("Connexion Okay", status=status.HTTP_201_CREATED)


@api_view(['POST'])
def connectionFunctionView(request, format=None):
    """
     connection with username and password
    """
    
    print(request.data['username'])
    print(request.data['password'])
    
    #return Response("Connexion Okay", status=status.HTTP_201_CREATED)
    try:
        password = make_password(request.data['password'])
        current_user = get_object_or_404(User, username=request.data['username'], password=password)

        user_serialized = UserSerializer(current_user).data

        user = User.objects.get(username=serializer.validated_data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
                #'username': str(user_serialized),
                'username': user_serialized,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'response': "Aucun compte n'est associe à ses informations"},
                        status=status.HTTP_404_NOT_FOUND)





class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



