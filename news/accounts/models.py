from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from news_db.models import Role

def user_avatar_path(instance, filename):
    email_folder = instance.user.email.replace('@', '_at_').replace('.', '_dot_')
    return f'users/avatar/{email_folder}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Роль')
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True)

    @property
    def user_role(self):
        if self.role:
            return self.role.title
        return "Не указана"

    def __str__(self):
        return f'Профиль {self.user.username}'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()