from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from.models import Tweet

class TweetForm(forms.ModelForm):
    content=forms.CharField(
        widget=forms.Textarea,
        max_length='1000',
        required=True,
        help_text='今の気持ちをつぶやこう'
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
