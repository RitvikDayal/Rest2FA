from django_otp.models import Device
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

from .models import TOTPClient


def get_totp_secret(user):
    """
    Get the TOTP secret for a user.
    """
    totp_client = TOTPClient.object.get(user=user)
    return totp_client.secret


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def blacklist_tokens(usertoken):
    """
    Logout a user.
    """
    try:
        token = RefreshToken(usertoken)
        token.blacklist()
        return True
    except Exception as e:
        print(e)
        return False


def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device


class TokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, device=None):
        token = super().get_token(user)

        token["name"] = user.get_full_name
        # custom additions
        if (
            (user is not None)
            and (device is not None)
            and (device.user_id == user.id)
            and (device.confirmed is True)
        ):
            token["otp_device_id"] = device.persistent_id
        else:
            token["otp_device_id"] = None

        return token


def get_tokens_for_user(user, device=None):
    """
    Get a token pair for a user.
    """
    serializer = TokenPairSerializer()
    refresh = serializer.get_token(user, device)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def otp_is_verified(self, request):
    """
    Helper to determine if user has verified OTP.
    """
    auth = JWTAuthentication()
    try:
        validation = auth.authenticate(request)
        if validation is not None:
            user, token = validation
            payload = token.payload
            persistent_id = payload.get("otp_device_id")

            if persistent_id:
                device = Device.from_persistent_id(persistent_id)
                if (device is not None) and (device.user_id != request.user.id):
                    return False
                else:
                    return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
