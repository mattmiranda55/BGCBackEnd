from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.hashers import make_password, check_password


class Regulation(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField()
    address = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("Please provide a valid email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        hashed_pwd = make_password(password)
        check_password(password, hashed_pwd)
        user.set_password(hashed_pwd)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(blank=True, default='', unique=True)
    email_address = models.EmailField(blank=True, default='', unique=True)
    first_name = models.CharField(blank=True, default='')
    last_name = models.CharField(blank=True, default='')
    password = models.CharField(blank=True, default='')
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email_address'

    objects = CustomUserManager()

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.username


class Graft(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
