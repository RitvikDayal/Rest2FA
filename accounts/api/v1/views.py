from django_otp import user_has_device
from rest_framework import generics, status, permissions, views
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
)
from accounts.utils import (
    get_user_totp_device,
    get_tokens_for_user,
    blacklist_tokens
)

from accounts.permissions import IsOtpVerified


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration view.
    This view provides a POST request that accepts the following parameters:
        - email: The email address
        - password: The password to be used for the user
        - first_name: The first name of the user
        - last_name: The last name of the user
    """

    throttle_scope = "anon_user"
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

    throttle_scope = "anon_user"
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


class LogoutHandlerView(APIView):
    """
    View for logging out a user
    """

    throttle_scope = "user"
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


class TOTPClientCreateView(views.APIView):
    """
    Add a new TOTP totp_device for a user.
    """

    throttle_scope = "user"
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get the TOTP totp_device for the current user.
        Setup a new TOTP totp_device for a user if it does not exist.
        """
        user = request.user

        if not user_has_device(user):
            totp_device = user.totpdevice_set.create(confirmed=False)
            url = totp_device.config_url
            return Response(url, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": "User already have active TOTP device"},
                status=status.HTTP_204_NO_CONTENT,
            )


class TOTPVerifyView(views.APIView):
    """
    Verify the TOTP token for the current user.
    """

    throttle_scope = "user"
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, token):
        """
        Verify the TOTP token for the current user.
        """
        user = request.user
        totp_device = get_user_totp_device(self, user)

        if not totp_device == None and totp_device.verify_token(token):
            if not totp_device.confirmed:
                totp_device.confirmed = True
                totp_device.save()

            prev_token = blacklist_tokens(request.data["refresh_token"])
            print(request.data)
            if prev_token:
                token = get_tokens_for_user(user, totp_device)
                return Response({"token": token}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProtectView(views.APIView):
    """
    Protect the API with a TOTP token.
    """

    throttle_scope = "user"
    permission_classes = [IsOtpVerified]

    def get(self, request):
        """
        Get the TOTP token for the current user.
        """
        user = request.user
        return Response(
            {"message": "Hello {}, You can view this.".format(user.get_full_name)},
            status=status.HTTP_200_OK,
        )
