"""Truckporter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from UserAuth import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.homepage),
    url(r'^forgot_password/', views.forgot_password),
    url(r'^reset_password/', views.reset_password),
    url(r'^login/', views.login_start),
    url(r'^dashboard/', views.show_dashboard),
    url(r'^referrals/', views.show_referrals),
    url(r'^contact_us/', views.show_contact_us),
    url(r'^about_us/', views.show_about_us),
    url(r'^profile/', views.show_profile),
    url(r'^logout/', views.logout_start),
    url(r'^accounts/login/', views.homepage),
    url(r'^ajax_change_password/$', views.ajax_change_password),

]
