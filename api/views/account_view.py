from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from api.models import User
from api.permissions import HasModelPerm
from api.serializers import RegisterSerializer, UserSerializer
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():

        user = serializer.save()
        return Response({"id":user.id,
                         "email":user.email,
                         "first_name":user.first_name,
                         "last_name":user.last_name,
                         "middle_name":user.middle_name})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"message":"требуются почта и пароль"},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    if user is None:
        return Response({"message":"неверные данные входа"},
                        status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "token":token.key,
        "user": {
            "id":user.id,
            "email":user.email,
            "first_name":user.first_name,
            "last_name":user.last_name,
            "middle_name":user.middle_name
        }},
        status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
def api_logout(request):
    request.user.auth_token.delete()
    return Response({"message": "logged out"})

class AccountView(APIView):

    def patch(self,request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # deactivate account
    def delete(self,request):
        user = User.objects.get(email=request.user.email)
        user.is_active=False
        user.save()
        return Response(UserSerializer(user).data)


class CanChangeUser(HasModelPerm): perm = "api.change_user"

class AccountDetailsView(APIView):
    def get_permissions(self):
        if self.request.method in ['PATCH','PUT']:
            return [CanChangeUser()]
        return super().get_permissions()

    # update user role, only admin has access to this endpoint
    def patch(self,request, pk):
        role = request.data.get('role','')
        if role:
            user = get_object_or_404(User, pk=pk)
            group = Group.objects.get(name=role.capitalize())
            if group is not None and group in user.groups.all():
                user.groups.remove(group)
            elif group is not None:
                user.groups.add(group)


        return Response("updating user details")