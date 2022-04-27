'''
各个模板标签的代码
'''
import random

from django import template
from django.db.models.aggregates import Count

from ..models import Post, Category, Tag, InviteCode

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }


# generate_code应该不需要了
@register.simple_tag
def generate_code():
    li_code = []
    for i in range(65, 91):  # 大写字母A-Z
        li_code.append(chr(i))
    for j in range(97, 123):  # 小写字母a-z
        li_code.append(chr(j))
    for k in range(48, 58):  # 数字0-9
        li_code.append(chr(k))
    code = random.sample(li_code, 10)
    ran_code = "".join(code)
    return ran_code


@register.simple_tag
def show_code():
    code_qr = InviteCode.objects.filter(state=0)
    code_li = list(code_qr)
    code = random.choice(code_li)
    # print(code)
    return code


