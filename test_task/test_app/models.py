import jwt
from django.template.defaultfilters import truncatechars
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True)
    name = '123'
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')



class Organization(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    address = models.TextField()
    postcode = models.CharField(max_length=10)
    users = models.ManyToManyField(User)

    @property
    def short_description(self):
        return truncatechars(self.description, 20)

    def __str__(self):
        return f"{self.title}"

    def get_full_address(self):
        return f"{self.address}, postcode: {self.postcode}"


class Event(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    organizations = models.ManyToManyField(Organization)
    image = models.ImageField()
    date = models.DateTimeField()

    @property
    def short_description(self):
        return truncatechars(self.description, 20)

    def __str__(self):
        return f"{self.title}"


class Message(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField(max_length=255)