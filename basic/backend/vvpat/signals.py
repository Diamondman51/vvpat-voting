from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Voter, Director, President

@receiver(post_save, sender=User)
def create_voter_director_president(sender, instance, created, **kwargs):
    if created:
        if instance.is_president:
            president = President.objects.create(
                first_name=instance.first_name,
                last_name=instance.last_name,
                image=instance.image,
                membership_num=instance.membership_num,
            )
        
        elif instance.is_director:
            director = Director.objects.create(
                first_name=instance.first_name,
                last_name=instance.last_name,
                image=instance.image,
                membership_num=instance.membership_num,
            )

        elif not instance.is_director and not instance.is_president or instance.is_employee:
            voter = Voter.objects.create(
                first_name=instance.first_name,
                last_name=instance.last_name,
                image=instance.image,
                user_id=instance,
            )
