from __future__ import absolute_import, unicode_literals

# Third Party Stuff
from django.contrib.auth.models import BaseUserManager

# djcms Stuff

from django.utils import timezone
import json


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
            self,
            email,
            password,
            username,
            is_staff,
            is_superuser,

            **extra_fields):
        """
        Creates and saves a User with the given email and password.

        """
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_superuser=is_superuser,

            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
            self,
            email,
            password=None,
            username='username',
            **extra_fields):
        today = timezone.now()
        username = today.strftime("user%Z%Y%m%d%H%M%S%f")
        user = self._create_user(
            email,
            password,
            username,
            False,
            False,
            3,
            **extra_fields)
        contexxt = {'Title': "",
                    'GivenName': user.first_name,
                    'MiddleName': "",
                    'FamilyName': user.last_name,
                    'Suffix': "Dr",
                    'Notes': "",
                    'FullyQualifiedName': user.username,
                    'CompanyName': "WLTDO",
                    'DisplayName': str(user.id)}
        user.save()

        return user

    def create_walker(
            self,
            email,
            password=None,
            username='username',
            **extra_fields):
        today = timezone.now()
        username = today.strftime("user%Z%Y%m%d%H%M%S%f")
        user = self._create_user(
            email,
            password,
            username,
            False,
            False,
            2,
            **extra_fields)
        contexxt = {'Title': "",
                    'GivenName': user.first_name,
                    'MiddleName': "",
                    'FamilyName': user.last_name,
                    'Suffix': "Dr",
                    'Notes': "",
                    'FullyQualifiedName': user.username,
                    'CompanyName': "WLTDO",
                    'DisplayName': str(user.id)}
        user.save()

        return user

    def create_superuser(
            self,
            email,
            password,
            username='username',
            **extra_fields):
        return self._create_user(
            email, password, username, True, True,  **extra_fields)

    def create_staffuser(
            self,
            email,
            password,
            username='username',
            **extra_fields):
        return self._create_user(
            email, password, username, True, False, 0, **extra_fields)
