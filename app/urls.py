from django.urls import path
from.views import IndexView,TweetCreateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', TweetCreateView.as_view(), name='tweet_create'),
]