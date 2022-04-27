from django import forms

from .models import Post


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    invitecode = forms.CharField(label="邀请码", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))


class InviteCodeForm(forms.Form):
    invitecode = forms.CharField(label="邀请码", max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))


class PostsForm(forms.ModelForm):
    author = forms.CharField(label="作者", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(label="标题", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label="正文", max_length=2000, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.CharField(label="分类", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tags = forms.CharField(label="标签", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        # 表明这个表单对应的数据库模型是 Post 类
        model = Post
        # 指定了表单需要显示的字段
        fields = ['author', 'title', 'body', 'category', 'tags']
