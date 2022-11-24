from .models import User, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance,created,**kwargs):
    print(created,'###########################################')
    if created:
        UserProfile.objects.create(user=instance)
        print('user profile created')
    else:
        try:
            profile=UserProfile.objects.get(user=instance)
            profile.save()
            print('user is updated')
        except:
            # Create the userprofile if not exist
            UserProfile.objects.create(user=instance)
