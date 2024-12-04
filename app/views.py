from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic import CreateView,ListView,DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from.models import Tweet,Like
from.forms import TweetForm,SignUpForm
from django.urls import reverse_lazy



# Create your views here.

class IndexView(ListView):
    model=Tweet
    template_name='app/index.html'
    context_object_name='tweets'
    ordering=['-created_at']
    paginate_by=5

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            return redirect('app:tweet_detail', pk=tweet.pk)
    else:
        form = TweetForm()
    return render(request, 'app/tweet_create.html', {'form':form})


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
            return redirect('app:index')
        else:
            return render(request, self.template_name, {'form':form})

def tweet_detail(request, pk):
    tweet = get_object_or_404(Tweet,pk=pk) #Djangoの関数。特定のモデルオブジェクトを取得

    is_liked = False #初期値をFolseで設定
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, tweet=tweet).exists() #Likeモデルに紐づく投稿があればis_like=Trueに

        context = {#contextでテンプレートにviewを辞書でわたす
            'tweet': tweet,
            'is_liked': is_liked,
            'like_count': tweet.likes.count(),
        }
        return render(request, 'app/tweet_detail.html', context)

class TweetDetailView(DetailView):
    model=Tweet
    template_name='app/tweet_detail.html'
