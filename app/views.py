from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import CreateView,ListView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from.models import Tweet
from.forms import TweetForm,SignUpForm
from django.urls import reverse_lazy



# Create your views here.

class IndexView(ListView):
    model=Tweet
    template_name='app/index.html'
    context_object_name='tweets'
    ordering=['-created_at']
    paginate_by=5

class TweetCreateView(LoginRequiredMixin,CreateView):
    model=Tweet
    form_class=TweetForm
    template_name='app/tweet_create.html'
    success_url=reverse_lazy('app:index')

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request, 'ツイートが投稿されました！')
        return super().form_valid(form)

class SignUpView(View):
    form_class=SignUpForm
    template_name='app/signup.html'

    #Viewを継承しているので自分で定義が必要。CreateViewやListViewはDjangoのgenericを使用しているので定義の必要がない。
    #self はクラス内のメソッドで、自身のインスタンス。
    #request は、Djangoが生成するHTTPリクエストオブジェクト。
    #ユーザーが送信した情報（GET/POSTデータ、ヘッダー、Cookieなど）が格納されています。
    def get(self,request):
        form=self.form_class()
        return render(request,self.template_name, {'form':form})

    def post(self,request):
        form=self.form_class(request.POST)#ユーザの入力を渡す
        if form.is_valid():
            user=form.save()
            login(request, user)
            messages.success(request, 'アカウントが作成され、ログインが成功しました！')#djangoのmessageフレームワーク
            return redirect('index')
        else:
            return render(request, self.template_name, {'form':form})
