from django import forms
from .models import Post, Topic

class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 10, 'placeholder': "What's new with you?"}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000 words')

    class Meta:
        model = Topic
        fields = ['subject', 'message']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
