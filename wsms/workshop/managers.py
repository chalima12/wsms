from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where  user_name is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, user_name, password, **extra_fields):
        """
        Create and save a user with the given user_name and password.
        """
        if not user_name:
            raise ValueError(_("The user_name must be set"))
        user_name = self.normalize_email(user_name)
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_name, password, **extra_fields):
        """
        Create and save a SuperUser with the given user_name and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(user_name, password, **extra_fields)