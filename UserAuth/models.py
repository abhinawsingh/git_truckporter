from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

'''class CustomUserManager(BaseUserManager):
	def create_user(self,username,first_name,last_name, email, password, mobile, dob, gender):
		user = self.model(username = username, first_name = first_name, last_name = last_name,
							email=email, mobile=mobile, dob = dob, gender=gender, is_staff=True,
							is_active=True, is_superuser=False, last_login=timezone.now(), 
						  date_joined=timezone.now())
		user.set_password(password)
		user.save(using=self._db)
		return user'''

class CustomUserManager(BaseUserManager):
	def create_user(self,username,first_name,last_name, email, mobile, dob, gender, password=None):
		user = self.model(username = username, first_name = first_name, last_name = last_name, email = email,
						  mobile = mobile, dob = dob, gender = gender)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self,username,first_name,last_name, email, mobile, dob, gender, password):
		user = self.create_user(username = username, first_name = first_name, last_name = last_name, email = email,
								mobile = mobile, dob = dob, gender = gender, password = password)
		user.is_staff = True
		user.is_admin = True
		user.save(using=self._db)
		return user
						  

class CustomUser(AbstractBaseUser, PermissionsMixin):
	first_name  =  models.CharField(max_length=30)
	last_name   =  models.CharField(max_length=30)

	username    =   models.CharField(max_length=30, unique=True)
	email       =   models.CharField(max_length=30)
	mobile      =   models.CharField(max_length=14, null=True, default="0000")
	dob 		=   models.DateField()
	gender      =   models.CharField(max_length=1, null=True, default="M")

	is_staff = models.BooleanField(_('staff status'), default=False)
	is_active = models.BooleanField(_('active'), default=True)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['first_name','last_name', 'email', 'mobile', 'dob']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_absolute_url(self):
		return "/users/%s/" % urlquote(self.email)

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return '%s %s' % (self.first_name, self.last_name[:1])

	def email_user(self, subject, message, from_email=None):
		send_mail(subject, message, from_email, [self.email])

