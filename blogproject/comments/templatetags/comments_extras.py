# 定义一个 inclusion_tag 类型的模板标签，用于渲染评论表单
from django import template

from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, user_name, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
        'user_name': user_name
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
