from django.urls import path
from.views import IndexView,TweetCreateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', TweetCreateView.as_view(), name='tweet_create'),

    #認証関連
    path('login/', auth_views,LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views,LogoutView.as_view(template_name='app/logout.html'), name='logout'),
]