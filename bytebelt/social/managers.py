from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Customer User model Manager where the email field is the unique identifier
    for authentication instead of username
    """
    def create(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The email field must be set to create a user'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
