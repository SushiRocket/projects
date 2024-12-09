from django import template
from app.models import Follow
from django.contrib.auth.models import User

register = template.library()#カスタムフィルタやテンプレートタグを登録し、それらをテンプレート内で使用できるようにする。

@register.filter #デコレータとして関数の上に付けることで、その関数をテンプレート内でフィルタとして使用可能にする。
def is_following(user,target_user):
#ユーザーがターゲットユーザーをフォローしているかを判定するフィルタ
    if user.is_authenticated:
        return Follow.objects.filter(follower=user, following=target_user).exists()
    return False

@register.filter
def follower_count(user):
    return user.follwers.count()

@register.filter
def following_count(user):
    return user.following.count()