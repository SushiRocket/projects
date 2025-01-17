from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.models import Tweet,Profile,Comment

class TweetForm(forms.ModelForm):
    content=forms.CharField(
        widget=forms.Textarea,
        max_length=1000,
        required=True,
        help_text='今の気持ちをつぶやこう',
    )

    class Meta:
        model = Tweet
        fields = ['content']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='必須。有効なメールアドレスを入力してください。'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("このメールアドレスは既に使用されています。")
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avator']
        widgets ={
            'avator': forms.ClearableFileInput(attrs={
                'class': 'profile-input',
                'placeholder': 'ファイルを選択してください',
                'accept': '.jpg, .png, .gif',
            })
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget = forms.Textarea(attrs={
            'placeholder': 'コメントを入力.....',
            'rows': 3,
        }),
        max_length = 500,
        required=True,
    )
    class Meta:
        model = Comment
        fields = ['content']

class CommentEditForm(forms.ModelForm):
    content = forms.CharField(
        widget = forms.Textarea(attrs={
            'placeholder': 'コメントを編集.....',
            'row': 3,
        }),
        max_length=500,
        required=True,
    )
    class Meta:
        model = Comment
        fields = ['content']

    def claen_parent(self):
        parent_id = self.cleaned_data.get('parent')
        if parent_id:
            try: #エラーが発生してもプログラムを停止させずに処理を続けるための方法。
                parent_comment = Comment.objects.get(pk=parent_id)#エラーが起きる可能性のあるコード
            except Comment.DoesNotExist:#エラー発生時のコード
                raise forms.ValidationError('親コメントが存在しません。')
            return parent_comment
        return None

class TweetSearchForm(forms.Form):
    query = forms.CharField(
        label='検索',
        max_length=100,
        required=False,
        widget= forms.TextInput(attrs={
            'placeholder': 'キーワードで検索',
        }),
    )