"""cowork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf.urls import include, url
from django.urls import include, path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from apps.user.views import FacebookLogin, GoogleLogin, AppleLogin
from apps.user.admin import event_admin_site

urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls', namespace='blog')),

    # provide the most basic login/logout functionality
    url(r'^login/$', auth_views.LoginView.as_view(template_name='core/login.html'),
        name='core_login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='core_logout'),
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', admin.site.urls),  # admin site
    path(r'merchant/portal/', event_admin_site.urls),

    url(r'api/auth/registration/', include('rest_auth.registration.urls')),
    path(r'api/auth/', include('rest_auth.urls')),
    path(r'api/auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path(r'api/auth/google/', GoogleLogin.as_view(), name='google_login'),
    path(r'api/auth/apple/', AppleLogin.as_view(), name='google_login'),
]
