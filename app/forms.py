from django import forms
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

class SignUpForm(forms.ModelForm):
    password1=forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput,
    )

    password2=forms.CharField(
        label='再確認用パスワード',
        widget=forms.PasswordInput
    )

    class Meta:
        model = 'User'
        fields = ('username', 'password1', 'password2')

    def clean_password2(self):
        password1=self.cleaned_data.get('password1') #validateを通過したものをget
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('パスワードが一致しません！')
        return password2

    def save(self, commit=True):
        user=super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1']) #set_passwordでパスワードのハッシュ化（djangoの組み込み関数）
        if commit:
            user.save()
            return user