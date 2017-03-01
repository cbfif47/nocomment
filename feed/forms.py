from django import forms

from .models import Post

class PostLike(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('liked','disliked')