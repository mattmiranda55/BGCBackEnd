from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.postgres.fields import ArrayField
from storages.backends.s3boto3 import S3Boto3Storage

# importing Django user model 
from django.contrib.auth.models import User 
from django.dispatch import receiver
from django.db.models.signals import post_save
import binascii




class Regulation(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Graft(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    purchase_link = models.CharField(blank=True, max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_by = models.CharField(null=True, max_length=200)
    documents = ArrayField(models.CharField(max_length=200), blank=True, null=True) 
    image = models.ImageField(upload_to='grafts/images/', storage=S3Boto3Storage(), null=True)
    validated = models.BooleanField(default=False)

    def get_image_url(self):
        # Convert the byte-like representation to a string
        if self.image and isinstance(self.image, bytes):
            return self.image.decode('utf-8', errors='ignore').replace("\\x", "")
        return None
    
    def __str__(self):
        return self.name
    
    








"""
Profile model extends the User model 

Includes addittional fields...
1. Credits 
2. BusinessName 
3. Phone Number 

"""
class Profile(models.Model):
    
    # import user model 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    num_credits = models.IntegerField(blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()