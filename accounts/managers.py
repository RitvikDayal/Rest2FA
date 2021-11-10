from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom User Manager For User.
    """

    use_in_migrations = True

    def create_user(self, email, first_name, password, **extra_fields):
        """
        This manager creates a simple user account for the given email.
        """
        if not email:
            raise ValueError(_("You must provide an email address."))

        # cleaning mail address.
        email = self.normalize_email(email)

        # creating user model object
        user = self.model(
            email=email, first_name=first_name, password=password, **extra_fields
        )

        # setting password for the user
        user.set_password(password)

        # saving user model instance
        user.save()

        return user

    def create_superuser(self, email, first_name, password, **other_fields):
        """
        This manager creates a super user account for the given email.
        """

        # setting superuser, staff, active status as true by default
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_admin", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_active", True)

        # checking for staff status
        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")

        # checking for superuser status
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        # Creating user account for superuser.
        return self.create_user(email, first_name, password, **other_fields)
