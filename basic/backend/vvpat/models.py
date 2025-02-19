import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, help_text="+998950701662")
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    birth_day = models.DateField(max_length=30, help_text="day.month.year (2004-01-06)", null=True, blank=True)
    gender = models.IntegerField(choices=[(1, 'Male'), (0, 'Female')], null=True, blank=True)
    membership_num = models.CharField(max_length=25, null=True, blank=True, unique=True)
    is_director = models.BooleanField(default=False)
    is_president = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ("username", "first_name", "last_name", "email", "birth_day", "gender")

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'
    
    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
    
    def save(self, *args, **kwargs):
        self.hashing_password()
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super().delete(*args, **kwargs)


class Voter(models.Model):
    # position = models.ForeignKey('Position', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(blank=False, null=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, to_field="uuid")
    president_vote = models.CharField(unique=False, null=True, blank=True, max_length=255)
    directors_vote = models.JSONField(null=True, blank=True, default=list)
    # random_num = models.IntegerField(default=0)
    # president_vote = models.ForeignKey('President', on_delete=models.SET_NULL, null=True, blank=True)  # Voter selects one president
    # directors_vote = models.ManyToManyField('Director', blank=True)  # Voter selects multiple directors
    is_voted = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super().delete(*args, **kwargs)


class Director(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    membership_num = models.CharField(max_length=255, null=True, blank=True)
    omr_votes = models.JSONField(null=True, blank=True, default=list)
    # side = models.IntegerField(max_length=10, choices=((0, 'Left'), (1, 'Right')), null=True, blank=False)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def delete(self, *args, **kwargs):
        self.image.delete()
        return super().delete(*args, **kwargs)


class President(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(blank=False, null=True)
    membership_num = models.CharField(null=True, blank=True, unique=True, max_length=255)
    omr_votes = models.JSONField(null=True, blank=True, default=list)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        return super().delete(*args, **kwargs)
