from django.db import models

class Vote(models.Model):
    candidate = models.CharField(max_length=100)

    def __str__(self):
        return self.candidate
