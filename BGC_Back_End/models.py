from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.hashers import make_password, check_password

# importing Django user model 
from django.contrib.auth.models import User 
from django.dispatch import receiver
from django.db.models.signals import post_save
    




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


class Graft(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.BinaryField(blank=True)
    purchase_link = models.URLField(blank=True)

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