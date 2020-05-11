from django import forms
from apps.operation.models import UserFavorite, CourseComment
import re
# class AddAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     mobile = forms.CharField(required=True, min_length=11, max_length=11)
#     course_name = forms.CharField(required=True, min_length=2, max_length=20)
#
# 从model中直接建立form
class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['fav_id', 'fav_type']

class CommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = ['course', 'comments']