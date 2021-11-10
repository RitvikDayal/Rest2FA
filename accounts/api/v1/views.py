import pyotp

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import TOTPClient
from accounts.permissions import Is2FAEnabled
from accounts.utils import blacklist_tokens, get_tokens_for_user
from .serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration view
    """

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        """
        User registration
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        return Response(
            {
                "message": "User Created Successfully",
                "user_email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        return serializer.save()


class UserLoginView(generics.RetrieveAPIView):
    """
    View for a user to login through 1FA.
    The view provides a post request that accepts a email and password.
    Returns a jwt token as a response to authenticated user.
    """

    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        POST request to login a user.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "success": "True",
            "message": "User logged in  successfully",
            "token": serializer.validated_data["tokens"],
            "user_name": serializer.validated_data["user_name"],
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class User2FARegistrationView(APIView):
    """
    View to register a user with 2FA
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """
        Generate a TOTP secret key and return it to the user
        """

        if request.user.is_2fa_enabled:
            return Response(
                {"error": "User already has 2FA enabled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        totp_client = TOTPClient.objects.create(
            user=request.user, secret=pyotp.random_base32(), label=request.user.email
        )
        totp_client.save()

        response = {
            "success": "True",
            "message": "TOTP secret key generated successfully",
            "secret_key": totp_client.secret,
            "issuer": "Django",
            "label": request.user.email,
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class User2FAAuthenticationView(generics.RetrieveAPIView):
    """
    View for authenticating a user with TOTP
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        POST request to authenticate a user with TOTP
        """

        data = self.request.data
        user = self.request.user
        totp_client = TOTPClient.objects.get(user=user)

        if totp_client.verify_totp(data["totp"]):
            # Saving 2_fa_enabled Check
            user.is_2fa_verified = True
            user.save()

            response = {
                "success": "True",
                "message": "User logged in  successfully",
                "token": get_tokens_for_user(user),
                "user_name": user.email,
            }
            status_code = status.HTTP_200_OK
        else:
            response = {
                "success": "False",
                "message": "TOTP is incorrect",
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)


class LogoutHandlerView(APIView):
    """
    View for logging out a user
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        POST request to logout a user
        """
        data = request.data
        if blacklist_tokens(data["token"]):
            response = {
                "success": "True",
                "message": "User logged out successfully",
            }
            status_code = status.HTTP_200_OK
        else:
            response = {
                "success": "False",
                "message": "User not logged out",
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)


class ProtectedView(APIView):
    """
    View for testing authentication
    """

    permission_classes = (Is2FAEnabled,)

    def get(self, request):
        """
        GET request to test authentication
        """
        response = {
            "success": "True",
            "message": "Authentication successful",
        }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)
