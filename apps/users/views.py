from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers import UserSerializer

User = get_user_model()


class SignupAPIView(generics.CreateAPIView):
    """
    Registration View
    Take 2 argument: username and password
    in form-data and return only status code.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginAPIView(ObtainAuthToken):
    """
    Login user
    Take 2 arguments : username and password
    in form-data and return Token
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status.HTTP_200_OK)
