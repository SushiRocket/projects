from django.shortcuts import render
from django.views.generic import TemplateView, CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from.models import Tweet
from.forms import TweetForm
from django.urls import reverse_lazy



# Create your views here.

class IndexView(ListView):
    model = Tweet
    template_name = 'app/index.html'
    context_object_name = 'tweets'
    ordering = ['-created_at']

class TweetCreateView(LoginRequiredMixin,CreateView):
    model = Tweet
    form_class = TweetForm
    template_name = 'app/tweet_create.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'ツイートが投稿されました！')
        return super().form_valid(form)
