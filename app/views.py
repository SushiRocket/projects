from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from.models import Tweet,Like,Follow,Comment
from.forms import TweetForm,SignUpForm,ProfileUpdateForm,CommentForm,CommentEditForm,TweetSearchForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden,JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.

class IndexView(ListView):
    model=Tweet
    template_name='app/index.html'
    context_object_name='tweets'
    ordering=['-created_at']
    paginate_by=5

def tweet_search(request):
    form = TweetSearchForm(request.GET or None) #まずは初期化。formやqueryやresultsを定義。
    query = ''
    results = []
    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            results = Tweet.objects.filter(
                Q(content__icontains=query) | Q(author__username__icontains=query)
            ).distinct().order_by('-created_at')

    paginator = Paginator(results,3)#1ページあたりの表示ツイート数
    page = request.GET.get('page')#urlパラメータからページ番号を取得

    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)#総ページ数を取得

    context = {
        'form': form,
        'query': query,
        'tweets':tweets,
    }
    return render(request, 'app/search_results.html', context)

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

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseForbidden('ログインが必要です。')

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.tweet = tweet
            comment.save()
            messages.success(request,'コメントが投稿されました！')
            return redirect('app:tweet_detail', pk=pk)
        else:
            messages.error(request, 'コメントの投稿に失敗しました。内容を確認してください。')

    else:
        comment_form = CommentForm()

    comments = tweet.comments.filter(parent__isnull=True).order_by('-created_at')#親コメントがない（トップレベルの）コメントのみを取得

    context = {#contextでテンプレートにviewを辞書でわたす
        'tweet': tweet,
        'is_liked': is_liked,
        'like_count': tweet.likes.count(),
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'app/tweet_detail.html', context)

@login_required
def delete_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    tweet_pk = comment.tweet.pk
    if comment.user != request.user:
        return HttpResponseForbidden('あなたはこのコメントを削除する権限がありません。')
    if request.method == 'POST':
        if request.user ==comment.user:
            comment.delete()
            messages.success(request, 'コメントが削除されました。')
            return redirect('app:tweet_detail', pk=tweet_pk)
    else:
        return render(request, 'app/delete_comment.html', {'comment': comment})

@login_required
def edit_comment(request,pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if comment.user != request.user:
        return HttpResponseForbidden('あなたはこのコメントを編集する権限がありません。')
    if request.method == 'POST':
        form = CommentEditForm(request.POST, instance=comment) #ユーザーの入力を渡す
        if form.is_valid():
            form.save()
            messages.success(request, 'コメントが更新されました！')
            return redirect('app:tweet_detail', pk=comment.tweet.pk)
    else:
        form = CommentEditForm(instance=comment)
    return render(request, 'app/edit_comment.html' , {'form': form})

@login_required
def add_reply(request, pk):

    #特定のコメントに対する返信ビュー
    parent_comment = get_object_or_404(Comment, pk=pk)
    tweet = parent_comment.tweet

    if request.method == 'POST':
        form = CommentForm(request.POST)#ユーザーの入力を渡す
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.tweet = tweet
            reply.parent = parent_comment
            reply.save()
            messages.success(request, '返信が投稿されました！')
            return redirect('app:tweet_detail', pk=tweet.pk)
        else:
            messages.error(request, '返信の投稿に失敗しました。内容を確認してください。')

    else:
        form = CommentForm(initial={'parent': parent_comment.pk})

    context = {
        'form': form,
        'parent_comment': parent_comment,
    }
    return render(request, 'app/add_reply.html', context)

@login_required
def tweet_edit(request,pk):
    tweet = get_object_or_404(Tweet,pk=pk)
    if tweet.author != request.user:
        return HttpResponseForbidden('あなたはこのツイートを編集する権限がありません。') #データは存在するがアクセス権限がないとき。メッセージ返せる。
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('app:tweet_detail', pk=tweet.pk)
    else:
        form = TweetForm(instance=tweet)
        return render(request, 'app/tweet_edit.html', {'form': form, 'tweet': tweet})

@login_required
def tweet_delete(request,pk):
    tweet = get_object_or_404(Tweet, pk=pk)
    if tweet.author != request.user:
        return HttpResponseForbidden('あなたはこのツイートを削除する権限がありません。')
    if request.method == 'POST':
        tweet.delete()
        return redirect('app:index')
    return render(request, 'app/tweet_delete.html', {'tweet': tweet})

@require_POST
@login_required
def like_toggle(request,pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)

        if not created:
            like.delete()
            liked=False
        else:
            liked=True
        like_count=tweet.likes.count()
        return JsonResponse({'liked': liked, 'like_count': like_count})

def user_profile(request, username): #URLからusernameを取得。path('user/<str:username>/', views.user_profile, name='user_profile')
    user = get_object_or_404(User, username=username)
    section = request.GET.get('section', 'tweets')

    if section == 'comments':
        comments = Comment.objects.filter(user=user).select_related('tweet').order_by('-created_at')
        tweets = [comment.tweet for comment in comments]

        paginator = Paginator(tweets, 3)
        page = request.GET.get('page')
        try:
            tweets_page = paginator.page(page)
        except PageNotAnInteger:
            tweets_page = paginator.page(1)
        except EmptyPage:
            tweets_page = paginator.page(paginator.num_pages)
        context = {
            'profile_user': user,
            'section': comments,
            'tweets': tweets_page,
            'is_paginated': tweets_page.has_other_pages(),
            'page_obj': tweets_page,
        }
    elif section == 'likes':
        likes = Like.objects.filter(user=user).select_related('tweet').order_by('-created_at')
        tweets = [like.tweet for like in likes]

        paginator = Paginator(tweets, 3)
        page = request.GET.get('page')
        try:
            tweets_page = paginator.page(page)
        except PageNotAnInteger:
            tweets_page = paginator.page(1)
        except EmptyPage:
            tweets_page = paginator.page(paginator.num_pages)
        context = {
            'profile_user': user,
            'section': likes,
            'tweets': tweets_page,
            'is_paginated': tweets_page.has_other_pages(),
            'page_obj': tweets_page,
        }
    else:
        tweets = Tweet.objects.filter(author=user).order_by('-created_at')
        paginator = Paginator(tweets, 3)
        page = request.GET.get('page')
        try:
            tweets_page = paginator.page(page)
        except PageNotAnInteger:
            tweets_page = paginator.page(1)
        except EmptyPage:
            tweets_page = paginator.page(paginator.num_pages)
        context = { #テンプレートに辞書で返す
            'profile_user': user,
            'section': tweets,
            'tweets': tweets_page,
            'is_paginated': tweets_page.has_other_pages(),
            'page_obj': tweets_page,
        }

    return render(request, 'app/user_profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile )#HTTP リクエストの内容を保持する属性
        if form.is_valid():
            form.save()
            messages.success(request, 'プロフィールが正常に更新されました！')
            return redirect ('app:user_profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'form': form
    }

    return render(request, 'app/edit_profile.html', context)

@login_required
@require_POST
def follow_toggle(request,username):
    target_user = get_object_or_404(User, username=username)
    if target_user == request.user:
        return JsonResponse({'error': '自分自身をふぉろーすることはできません'}, status=400)
    
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)

    if not created:
        follow.delete()
        following=False

    else:
        following=True
    
    follower_count = target_user.follower.count()
    following_count = target_user.following.count()

    return JsonResponse({
        'following': following,
        'follower_count': follower_count,
        'following_count': following_count,
    })