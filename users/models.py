from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password

from config import EMAIL_VERIFY_TOKEN_LIFETIME, PASSWORD_RESET_TOKEN_LIFETIME
from users.utils import generate_random_code, generate_uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not password:
            raise ValueError('The password must be set')
        if not validate_password(password, user=None):
            raise ValueError('The given password must be at least 8 characters long')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The mail id must be set')
        if not password:
            raise ValueError('The password must be set')

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('email_confirmed', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='Имя пользователя',
        blank=True,
        null=True,
        max_length=128,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=128,
        error_messages={
            'required': 'Пожалуйста, заполните поле пароля.',
        }
    )

    email = models.EmailField(
        verbose_name='Почта',
        unique=True,
        error_messages={
            'required': 'Пожалуйста, заполните поле почты.',
        }
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=100,
        error_messages={
            'required': 'Пожалуйста, заполните поле имени.',
        }
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=100,
        error_messages={
            'required': 'Пожалуйста, заполните поле фамилии.',
        }
    )
    number = models.CharField(verbose_name='Номер телефона', max_length=100, blank=True)
    date_joined = models.DateTimeField(verbose_name='Дата создания аккаунта', default=timezone.now)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='avatars/', null=True, blank=True)

    email_confirmed = models.BooleanField(
        default=False,
        verbose_name='Подтверждение почты',
        help_text='Прошел ли пользователь проверку почты после регистрации.'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

class EmailVerify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    code = models.IntegerField(default=generate_random_code)
    url = models.CharField(default=generate_uuid, editable=False, max_length=36)
    created_date = models.DateTimeField(auto_now_add=True)

    def is_expired(self) -> bool:
        expiration_time = timedelta(hours=EMAIL_VERIFY_TOKEN_LIFETIME)
        return timezone.now() > self.created_date + expiration_time

    def __str__(self):
        return f"Токен подтверждения почты: {User.objects.get(pk=self.pk).email}"

    class Meta:
        verbose_name = "Токен-верификации почты"
        verbose_name_plural = "Токены-верификации почты"

class PasswordReset(models.Model):
    email = models.EmailField(unique=True)
    code = models.IntegerField(default=generate_random_code)
    url = models.CharField(default=generate_uuid, editable=False, max_length=36)
    created_date = models.DateTimeField(auto_now_add=True)

    def is_expired(self) -> bool:
        expiration_time = timedelta(hours=PASSWORD_RESET_TOKEN_LIFETIME)
        return timezone.now() > self.created_date + expiration_time

    class Meta:
        verbose_name = "Токен-сброс почты"
        verbose_name_plural = "Токены-сброса почты"