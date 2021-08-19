from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django import forms
from .models import User
from django.contrib.admin import AdminSite
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class AdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.
    """
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': _(
            "Please enter the correct %(username)s and password for a staff "
            "account. Note that both fields may be case-sensitive."
        ),
    }
    required_css_class = 'required'

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )
        if not user.registers.filter(register_type='2').exists():
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name}
            )


class MerchantAdminSite(AdminSite):
    login_form = AdminAuthenticationForm
    site_header = "Merchant Admin Site"
    site_title = "Merchant Admin Portal"
    index_title = "Welcome to Merchant Admin Site"


event_admin_site = MerchantAdminSite(name='event_admin')
# Register your models here.


class MyUserCreationForm(DjangoUserCreationForm):

    class Meta:
        model = User
        fields = ("email",)


class MyUserChangeForm(DjangoUserChangeForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'readonly': 'readonly', 'placeholder': '***************'}),
        help_text=("Password can\'t be viewed, but can be changed " " using <a style='font-size: 13px; color: #653aa0' href=\"../password/\"><i>Password change form</i></a>."))

    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    model = User


    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', )}),
        ('Personal info', {'fields': (
            'first_name', 'last_name',
        )}),

    )
    add_fieldsets = (
        ("Basic", {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created', 'modified', 'get_full_name')
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'get_full_name', )
    list_display_links = ('email', )
    list_filter = ('is_email_verified',)
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
