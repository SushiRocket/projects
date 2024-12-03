from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from.models import Tweet
from.forms import TweetForm
from django.urls import reverse_lazy



# Create your views here.

class IndexView(TemplateView):
    template_name = 'app/index.html'

class TweetCreateView(LoginRequiredMixin,CreateView):
    model = Tweet
    form_class = TweetForm
    template_name = 'app/tweet_form.html'
    success_url = reverse_lazy('app/index.html')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self,request, 'ツイートが投稿されました！')
        return super().form_valid(form)