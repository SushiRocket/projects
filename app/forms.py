from django import forms

class TweetForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea,
        max_length='1000',
        required=True,
        help_text='今の気持ちをつぶやこう'
    )

    class Meta:
        model = Tweet
        fiels = ['content']