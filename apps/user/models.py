from django.db import models
from ..basic.models import TimeStampedUUIDModel
from .managers import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

REGISTER_TYPE = (
    ('0', "Admin"),
    ('1', _('User')),
    ('2', _('Merchant Manager')),
    ('3', _('Subordinate')),
)


# Create your models here.
class User(AbstractBaseUser, TimeStampedUUIDModel, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=225,
        unique=True)
    first_name = models.CharField(_('First Name'), max_length=120, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=120, blank=True)
    email = models.EmailField(_('email address'), db_index=True, unique=True)
    is_email_verified = models.BooleanField(default=False)
    is_generated = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text='Designates whether the user '
                  'can log into this admin site.')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ('-created', )

    def __str__(self):
        return "{}  --  {}".format(
            self.get_full_name.title(),
            self.email)

    @property
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(
            self.first_name.capitalize(),
            self.last_name.capitalize())
        return full_name.strip()
    get_full_name.fget.short_description = "Full Name"


class UserRegistration(TimeStampedUUIDModel):
    user = models.ForeignKey('user.User', related_name='registers', on_delete=models.CASCADE)
    register_type = models.CharField(max_length=1, choices=REGISTER_TYPE)
    publisher = models.ForeignKey('user.User', related_name='pub_register', blank=True, null=True,
                                  on_delete=models.SET_NULL)
    menu = JSONField()
    objects = models.Manager()

    class Meta:
        verbose_name = _('User Registration Type')
        verbose_name_plural = _('User Registration Type')
        ordering = ['-created']

    def __str__(self):
        return str(self.user.first_name)
