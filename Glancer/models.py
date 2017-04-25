from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

#User profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)

#Profile automatically created/updated when we create/update User instances
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


#Glance model. Defines Glance (Point) class
class Glance(models.Model):
    value = 1
    date = models.DateTimeField('Date Sent')
    description = models.TextField(max_length=200, blank=True)
    sender = models.ForeignKey( Profile, related_name="glance_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name="glance_receiver", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date, self.receiver.user.first_name)
