from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

    def total_likes(self):
        return self.likes.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f"{self.user.username} likes {self.tweet.id}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avator = models.ImageField(
        upload_to='avators',
        default='avators/default.png',
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"