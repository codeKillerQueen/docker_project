# 表单数据
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        # 表明这个表单对应的数据库模型是 Comment 类
        model = Comment
        # 指定了表单需要显示的字段
        fields = ['text']
