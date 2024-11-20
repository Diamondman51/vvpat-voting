from django.db import models

# Create your models here.

class Voter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.ForeignKey('Position', on_delete=models.CASCADE)
    image = models.ImageField(blank=False, null=True)
    president_id = models.ForeignKey('President', on_delete=models.CASCADE)
    directors_id = models.OneToOneField('Director', null=True, blank=True, on_delete=models.CASCADE)


class Director(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(blank=False, null=True)


class President(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(blank=False, null=True)


class Position(models.Model):
    position = models.CharField(max_length=255)
