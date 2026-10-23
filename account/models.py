from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен для создания пользователя")

        if not password:
            raise ValueError("Пароль обязателен для создания пользвоателя")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True")

        if extra_fields.get("is_active") is not True:
            raise ValueError("Суперпользователь должен иметь is_active=True")

        return self.create_user(email, password, **extra_fields)


class EmailUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    email = models.EmailField(
        verbose_name="email",
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="имя",
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(verbose_name="фамилия", max_length=30, blank=True)
    is_active = models.BooleanField(
        verbose_name="online",
        default=True,
    )
    is_staff = models.BooleanField(
        verbose_name="admin",
        default=False,
    )
    date_joined = models.DateTimeField(
        verbose_name="registrer date",
        default=timezone.now,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_short_name(self):
        return self.first_name or self.email


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Расширенный профиль пользвателя'
        verbose_name_plural = 'Расширенные профили пользователей'

        
    user = models.OneToOneField(
        to='EmailUser',
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='user'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='avatar'
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='city'
    )
    description = models.TextField(
        blank=True,
        verbose_name='about me'
    )

    def __str__(self) -> str:
        return f'Профиль: {self.user.email}'