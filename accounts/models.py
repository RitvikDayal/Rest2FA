import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model, it reflects the User table.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    first_name = models.CharField(_("First Name"), max_length=250)
    last_name = models.CharField(_("Last Name"), max_length=250)
    mobile_number = PhoneNumberField(_("Mobile number"), null=True, unique=True)
    email = models.EmailField(_("Email Address"), max_length=200, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)

    is_email_verified = models.BooleanField(_("Email Verified"), default=False)
    is_mobile_verified = models.BooleanField(_("Mobile Number Verified"), default=False)
    is_2fa_enabled = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return f"{self.first_name} | {self.email}"

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    @property
    def get_full_name(self):
        """
        Return first and last name.
        Return first name only if last name is not present
        """
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


class TOTPClient(models.Model):
    """
    Model to store TOTP client details.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    issuer = models.CharField(max_length=250, default="REST2FA")
    label = models.CharField(max_length=250, null=True, blank=True)
    secret = models.CharField(max_length=64)
    last_used = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.user.first_name} | {self.issuer} | {self.label}"

    def verify_totp(self, totp):
        """
        Verify TOTP.
        """
        from pyotp import TOTP

        totp_client = TOTP(self.secret)
        print(totp_client.now())
        return totp_client.verify(totp)
