from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
# from django.contrib.auth.forms import PasswordResetForm
from allauth.socialaccount.models import SocialAccount
from rest_framework import serializers, exceptions


from decimal import Decimal
# import reverse_geocoder as rg
import datetime


from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import requests as basic_request
from rest_framework.serializers import raise_errors_on_nested_writes, model_meta
from asgiref.sync import async_to_sync

from rest_framework import serializers, exceptions
from django import forms

from django.contrib.sites.shortcuts import get_current_site
from django.core import exceptions
from django.core.mail import EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.safestring import mark_safe
from django.template import loader
from django.contrib.auth.forms import default_token_generator
from django.db.models.functions import Lower
import unicodedata
import traceback
import json

from .models import User

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,)
    from allauth.account.adapter import get_adapter

except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

UserModel = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(style={"input_type": "password"}, required=True)
    # password2 = serializers.CharField(style={"input_type": "password"}, required=True)
    # country_code = serializers.IntegerField()
    # phone = serializers.IntegerField()
    # device_id = serializers.CharField(allow_blank=True)
    # os_type = serializers.CharField(required=True)
    # device_token = serializers.CharField(allow_blank=True)
    # emergency_contact_number = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name',  'email', 'password1',)

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),

        }

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    # def validate(self, data):
    #     if data['password1'] != data['password2']:
    #         raise serializers.ValidationError(_("The two password fields didn't match."))
    #     return data

    def _save_user(self, request, user, commit=True):
        data = self.get_cleaned_data()

        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')
        email_address = data.get('email')
        first_part = email_address.split("@")[0]
        second_part = email_address.split("@")[1].split(".")[0]
        user.username = "{}_{}".format(first_part, datetime.datetime.now().strftime("%j%H%M%s"))
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        # user.country_code = data.get('country_code')


        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

        return user

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        self._save_user(request, user, self)
        return user



class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """


    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'first_name', 'last_name', 'email')


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})
    # device_id=serializers.CharField(allow_blank=True)
    # os_type=serializers.CharField(required=True)
    # device_token=serializers.CharField(allow_blank=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = self._validate_email(email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)


        return user

def _unicode_ci_compare(s1, s2):
    """
    Perform case-insensitive comparison of two identifiers, using the
    recommended algorithm from Unicode Technical Report 36, section
    2.11.2(B)(2).
    """
    return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % email_field_name: email,
        })
        return (
            u for u in active_users
            if u.has_usable_password() and
            _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name='registration/password_reset_email_html.html',
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            user_email = getattr(user, email_field_name)
            site_name = request.GET.get('site_name', site_name)
            context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )



class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)

        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        if not User.objects.filter(email__iexact=self.validated_data.get('email')).exists():
            raise serializers.ValidationError("There is no user registered with the specified email address!")
        if SocialAccount.objects.filter(user__email=self.validated_data.get('email')).exists():
            raise serializers.ValidationError("FB users cannot reset password here ")

        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)
