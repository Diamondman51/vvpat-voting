from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Voter, Director, President
from django.contrib import messages

@receiver(post_save, sender=User)
def create_voter_director_president(sender, instance: User, created, **kwargs):
    request = getattr(instance, '_request', None)
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
            instance.is_employee = True
            

    if not created:
        if instance.is_president:
            is_exist = President.objects.filter(membership_num=instance.membership_num).exists()
            
            try:
                Director.objects.filter(membership_num=instance.membership_num).delete()
                # messages.success(request, 'Director deleted')
            except Director.DoesNotExist as e:
                pass
            try:
                Voter.objects.filter(user_id=instance.uuid).delete()
                # messages.success(request, 'Voter deleted')
            except Voter.DoesNotExist as e:
                pass
            if not is_exist:
                president = President.objects.create(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    image=instance.image,
                    membership_num=instance.membership_num,
                )

            else:
                president = President.objects.filter(
                membership_num=instance.membership_num,
            ).update(
                first_name=instance.first_name,
                last_name=instance.last_name,
                image=instance.image,
            )
                
        
        elif instance.is_director:
            is_exist = Director.objects.filter(membership_num=instance.membership_num).exists()
            try:
                President.objects.filter(membership_num=instance.membership_num).delete()
                # messages.success(request, 'President is deleted')
            except President.DoesNotExist as e:
                pass
            try:           
                Voter.objects.filter(user_id=instance.uuid).delete()
                # messages.success(request, 'Voter deleted')
            except Voter.DoesNotExist as e:
                pass
            
            if not is_exist:
                director = Director.objects.create(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    image=instance.image,
                    membership_num=instance.membership_num,
                )
            else:
                director = Director.objects.filter(
                membership_num=instance.membership_num,
            ).update(
                first_name=instance.first_name,
                last_name=instance.last_name,
                image=instance.image,
                )
                

        elif not instance.is_director and not instance.is_president or instance.is_employee:
            instance.is_employee = True
            is_exist = Voter.objects.filter(user_id=instance.uuid).exists()
            try:
                President.objects.filter(membership_num=instance.membership_num).delete()
                # messages.success(request, 'President is deleted')
            except President.DoesNotExist as e:
                pass
            try:
                Director.objects.filter(membership_num=instance.membership_num).delete()
                # messages.success(request, 'Director deleted')
            except Director.DoesNotExist as e:
                pass            
            if not is_exist:    
                voter = Voter.objects.create(
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    image=instance.image,
                    user_id=instance,
                )

            else:
                voter = Voter.objects.filter(
                user_id=instance,
            ).update(
                first_name=instance.first_name,
                last_name=instance.last_name,
                image=instance.image,
            )
            