from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
	def create_user(self, login, password):
		user = self.model(login=login, password=password)
		user.set_password(password)
		user.is_staff = False
		user.is_superuser = False
		user.save(using=self._db)
		return user

	def create_staffuser(self, login, password):
		user = self.model(login=login, password=password)
		user.set_password(password)
		user.is_staff = True
		user.is_superuser = False
		user.save(using=self._db)
		return user

	def create_superuser(self, login, password):
		user = self.model(login=login, password=password)
		user.set_password(password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

	def get_by_natural_key(self, login):
		return self.get(login=login)


class CustomUser(AbstractBaseUser, PermissionsMixin):
	login = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=30)
	is_superuser = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'login'
	objects = CustomUserManager()

	def __str__(self):
		return self.login