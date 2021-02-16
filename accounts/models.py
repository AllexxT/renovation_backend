from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from twilio.rest import Client


class CustomUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser(email, password, **extra_fields)

    def _create_user(self, email, password, username=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    email = models.EmailField(
        error_messages={'unique': 'A user with that email already exists.'},
        blank=False,
        max_length=254,
        verbose_name=_('Email address'),
        unique=True
    )

    username = models.CharField(
        _('Username'), max_length=150, blank=True, null=True
    )

    business_name = models.CharField(
        _('Business name'), max_length=64, blank=True
    )

    phone_number = PhoneNumberField(
        _("Phone number"),
        max_length=17,
        blank=True,
        null=True,
        unique=True
    )

    @property
    def get_number(self):
        return self.phone_number.as_e164

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()


class SMSModel(models.Model):
    number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.number)
