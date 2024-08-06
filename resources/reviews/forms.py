from django import forms
from resources.reviews.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered textarea-xs w-full',
                'placeholder': 'Write your comment here...'
            })
        }
