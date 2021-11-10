from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status

from django_otp import user_has_device

from accounts.utils import get_user_totp_device, get_tokens_for_user, blacklist_tokens
from accounts.permissions import IsOtpVerified


class TOTPClientCreateView(views.APIView):
    """
    Add a new TOTP totp_device for a user.
    """

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
