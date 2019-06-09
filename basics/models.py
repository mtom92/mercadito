from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField

USER_CHOICES = (
 ('business_owner', 'Business Owner'),
 ('user', 'User'),
)



class MyUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    type_of_user = models.CharField(max_length=100, choices=USER_CHOICES, default='user')
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['date_of_birth', 'email']
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='media/', null=True, blank=True)

    @receiver(post_save, sender=MyUser)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

class TypeBusiness(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Category(models.Model):
    type_of_business = models.ForeignKey(TypeBusiness, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Business(models.Model):
    owner = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=100)
    telephone = PhoneNumberField()
    type_of_business = models.ForeignKey(TypeBusiness, on_delete=models.SET_NULL, null=True)
    category= models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location_latitude = models.CharField('Latitude', max_length=20, null=True, blank=True)
    location_longitude = models.CharField('Longitude', max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to='media/', null=True, blank=True)
    logo = models.ImageField(upload_to='media/', null=True, blank=True)
