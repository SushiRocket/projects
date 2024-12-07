#djangoの機能。特定のイベント発生時に発生する特定の処理を実行する仕組み
from django.db.models.signals import post_save
from django.dispatch import receiver #シグナルの処理を紐づけるためのデコレーター
from django.contrib.auth.models import User
from.models import Profile

@receiver(post_save, sender=User)#Userモデルにたいして動作
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()