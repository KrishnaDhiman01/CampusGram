from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    # Ensure you have 'pillow' installed for ImageField to work
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile.png', blank=True, null=True)

    def __str__(self):
        return self.user.username

# --- SIGNALS ---
# These functions run automatically when a User is created.
# They create a matching Profile for that user.

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()