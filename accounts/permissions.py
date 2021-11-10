from rest_framework.permissions import BasePermission
from django_otp import user_has_device
from accounts.utils import otp_is_verified


class Is2FAEnabled(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.is_2fa_verified
            and request.user.is_active
            or request.user.is_superuser
        )


class IsOtpVerified(BasePermission):
    """
    If user has verified TOTP device, require TOTP OTP.
    """

    message = "You do not have permission to perform this action until you verify your OTP device."

    def has_permission(self, request, view):
        if user_has_device(request.user):
            return (
                request.user.is_authenticated
                and otp_is_verified(self, request)
                and request.user.is_active
            )
        else:
            return False
