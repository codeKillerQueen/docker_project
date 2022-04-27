from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from pure_pagination.mixins import PaginationMixin

from .models import Post, Category, Tag


# IndexView 的功能是从数据库中获取文章（Post）列表
# ListView 就是从数据库中获取某个模型列表数据的，所以 IndexView 继承 ListView
class IndexView(PaginationMixin, ListView):
    # 将 model 指定为 Post，告诉 django 我要获取的模型是 Post
    model = Post
    # 指定这个视图渲染的模板
    template_name = 'blog/index.html'
    # 指定获取的模型列表数据保存的变量名，这个变量会被传递给模板
    context_object_name = 'post_list'
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 6


class CategoryView(IndexView):
    # 覆写了父类的 get_queryset 方法
    # 该方法默认获取指定模型的全部列表数据,为了获取指定分类下的文章列表数据，我们覆写该方法，改变它的默认行为
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=t)


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year,
                                                              created_time__month=month)


# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response


from django.contrib import messages


def search(request):
    '''
    用户通过表单 get 方法提交的数据 Django 为我们保存在 request.GET 里
    这是一个类似于 Python 字典的对象，所以我们使用 get 方法从字典里取出键 q 对应的值
    即用户的搜索关键词。这里字典的键之所以叫 q 是因为我们的表单中搜索框 input 的 name 属性的值是 q
    如果修改了 name 属性的值，那么这个键的名称也要相应修改。
    '''
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    # 前缀 i 表示不区分大小写
    # Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})


from django.shortcuts import redirect
from django.contrib.auth import authenticate

from django.shortcuts import render

from django.contrib.auth.models import User
from django.db.models import Q
# 继承View 实现基于类的用户登陆
from django.views.generic.base import View


class LoginView(View):
    # 将 model 指定为 Post，告诉 django 我要获取的模型是 Post
    model = User
    # 指定这个视图渲染的模板
    template_name = 'blog/login.html'

    # 会根据 method 调用 post或者get方法
    def get(self, request):
        # 如果method为 GET 重新返回登陆页面
        return render(request, "blog/login.html", {})


from .forms import UserForm, RegisterForm, PostsForm


def signin(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        msg = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # print(username,password)
            try:
                user = User.objects.get(username=username)
                if authenticate(username=username, password=password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.username
                    return redirect('/index/')
                    # return render(request, 'blog/index.html', locals())
                else:
                    msg = "密码不正确！"
            except:
                msg = "用户不存在！"
        return render(request, 'blog/login.html', locals())

    login_form = UserForm()
    return render(request, 'blog/login.html', locals())


def signout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    # return redirect("/index/")
    return render(request, 'blog/login.html', locals())


class RegisterView(View):
    # 将 model 指定为 Post，告诉 django 我要获取的模型是 Post
    model = User
    # 指定这个视图渲染的模板
    template_name = 'blog/register.html'

    def get(self, request):
        return render(request, "blog/register.html")


from django.contrib.auth.hashers import make_password
from .models import InviteCode


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        message = "登录状态不允许注册！"
        return redirect("/index/")
    if request.method == "POST":
        # print('post part')
        register_form = RegisterForm(request.POST)
        # print(register_form)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            invitecode = register_form.cleaned_data['invitecode']
            # print(username, password1, email, invitecode)
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'blog/register.html', locals())
            else:
                same_name_user = User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'blog/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'blog/register.html', locals())
                try:
                    check_code = InviteCode.objects.get(invitecode=invitecode)
                    if check_code.state == 1:
                        message = '邀请码已被使用！'
                        return render(request, 'blog/register.html', locals())
                except:
                    message = '邀请码无效！'
                    return render(request, 'blog/register.html', locals())

                new_user = User.objects.create()
                new_user.username = username
                new_user.password = make_password(password1)
                new_user.email = email
                new_user.save()
                # 当一切都OK的情况下，创建新用户，并将邀请码置为失效状态
                check_code.state = 1
                check_code.used_by = new_user
                check_code.save()
                # return redirect('/login/')  # 自动跳转到登录页面
                return render(request, 'blog/login.html', locals())
    # print('form not valid part')
    register_form = RegisterForm()
    return render(request, 'blog/register.html', locals())


class GenetareCodeView(View):
    # 将 model 指定为 Post，告诉 django 我要获取的模型是 Post
    model = InviteCode
    # 指定这个视图渲染的模板
    template_name = 'blog/generate_code.html'

    def get(self, request):
        return render(request, "blog/generate_code.html")


import random


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


def generatecode(request):
    # 通过session再次验证
    if not request.session.get('is_login', None):
        # 未登录则跳转登录
        message = "请登录！"
        return render(request, 'blog/login.html', locals())
    if request.session.get('user_name') != 'hwt':
        # 如用户不是hwt
        message = "非管理员禁止访问！"
        return redirect("/index/")
    # if request.method == "POST":
    #     invitecode_form = InviteCodeForm(request.POST)
    #     if invitecode_form.is_valid():  # 获取数据
    #         # invitecode = invitecode_form.cleaned_data['invitecode']
    #         invitecode = generate_code()
    #         print(invitecode)
    #         if invitecode is not None and invitecode != '':
    #             new_code = InviteCode.objects.create()
    #             new_code.invitecode = invitecode
    #             new_code.save()
    #         return render(request, 'blog/generate_code.html', locals())

    # 不使用表单
    if request.method == "POST":
        invitecode = generate_code()
        # print(invitecode)
        if invitecode is not None and invitecode != '':
            new_code = InviteCode.objects.create()
            new_code.invitecode = invitecode
            new_code.save()
        return render(request, 'blog/generate_code.html', locals())
    return render(request, 'blog/login.html', locals())


class MakePostsView(View):
    # 将 model 指定为 Post，告诉 django 我要获取的模型是 Post
    model = Post
    # 指定这个视图渲染的模板
    template_name = 'blog/make_posts.html'
    # 指定获取的模型列表数据保存的变量名，这个变量会被传递给模板
    context_object_name = 'categories'

    def get(self, request):
        categories = Category.objects.all()
        return render(request, "blog/make_posts.html", {'categories': categories})


# def makeposts(request):
#     # print(request.POST)
#     if request.method == "POST":
#         print('--------------post method:', request.method)
#         post_form = PostsForm(request.POST) #.fields(title,body,category,tags)
#         # post_form.fields=(author,title,body,category,tags)
#         print(post_form)
#         # msg = "请检查填写的内容！"
#         if post_form.is_valid():
#             print('form is valid')
#             # author = request.session.get('user_name')
#             author_id = User.objects.get(username=request.session.get('user_name'))
#             title = post_form.cleaned_data['title']
#             body = post_form.cleaned_data['body']
#             category = post_form.cleaned_data['category']
#             tags = post_form.cleaned_data['tags']
#             tag_list = tags.split(' ')
#             print(author_id, title, body, category, tags)
#
#             new_post = Post.objects.create(
#                 author_id=author_id,
#                 title=title,
#                 body=body,
#                 category_id=Category.objects.get(name=category),
#             )
#
#             for t in tag_list:
#                 try:
#                     t_id = Tag.objects.get(name=t).id
#                     new_post.tags.add(t_id)
#                 except:
#                     new_t = Tag.objects.create(name=t).id
#                     new_post.tags.add(new_t)
#             new_post.save()
#             msg = "文章发布成功！"
#         else:
#             print(post_form)
#             msg = "请检查填写的内容！"
#         return render(request, 'blog/make_posts.html', locals())
#     else:
#         print('--------------other method:',request.method)
#     return render(request, 'blog/make_posts.html', locals())

def makeposts(request):
    # print(request.POST)
    if request.method == "POST":
        # print('--------------post method:', request.method)
        # author = request.session.get('user_name')
        author_id = User.objects.get(username=request.session.get('user_name')).id
        title = request.POST.get('title')
        body = request.POST.get('body')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        tag_list = tags.split(' ')
        # print(author_id, title, body, category, tags)
        new_post = Post.objects.create(
            author_id=author_id,
            title=title,
            body=body,
            category_id=Category.objects.get(name=category).id,
        )
        for t in tag_list:
            try:
                t_id = Tag.objects.get(name=t).id
                new_post.tags.add(t_id)
            except:
                new_t = Tag.objects.create(name=t).id
                new_post.tags.add(new_t)
        new_post.save()
        msg = "文章发布成功！"
        return render(request, 'blog/detail.html', {'post': new_post, 'msg': msg})
    return render(request, 'blog/make_posts.html', locals())


# class EditPostView(UpdateView):
#     model = Post
#     # context_object_name = 'form'
#     # form_class = PostsForm
#     template_name = 'blog/edit_post.html'
#     fields = ['author', 'title', 'body', 'category', 'tags']

class EditPostView(UpdateView):
    model = Post
    context_object_name = 'form'
    form_class = PostsForm
    template_name = 'blog/edit_post.html'

    # fields = ['author', 'title', 'body', 'category', 'tags']

    def get(self, request, *args, **kwargs):
        # 1
        # post = Post.objects.get(id=self.kwargs['pk'])
        # initial = {'name': adv_positin.name}
        # form = self.form_class(initial)
        # form = self.form_class(instance=post)
        # 2
        categories = Category.objects.all()
        post = get_object_or_404(Post, pk=kwargs['pk'])
        # category = Category.objects.filter(name=post.category).first()
        # print(category, type(category))
        # initial = {'author': post.author, 'body': post.body, 'category': category}
        # form = self.form_class(initial)
        form = self.form_class(instance=post)

        return render(request, 'blog/edit_post.html', {'form': form, 'categories': categories})

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        post.body = request.POST.get('body')
        # print('category',request.POST.get('category'))
        category_id = Category.objects.get(name=request.POST.get('category')).id
        post.category_id = category_id
        # print(category_id)
        post.save()
        msg = '文章修改成功！'
        # print(message)
        # return redirect('/index/')
        return render(request, 'blog/detail.html', {'post': post, 'msg': msg})


from django.urls import reverse_lazy


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    # msg = '删除成功！'
    success_url = reverse_lazy('blog:index')


class AboutView(IndexView):
    template_name = 'blog/about.html'

class ContactView(IndexView):
    template_name = 'blog/contact.html'