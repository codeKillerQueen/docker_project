from django.urls import path

from . import views

# django 会从用户访问的 URL 中自动提取 URL 路径参数转换器 <type:name> 规则捕获的值
# 然后传递给其对应的视图函数
urlpatterns = [
    path('', views.LoginView.as_view(), name='to_login'),
    path('api/login/', views.signin, name='login'),
    path('api/logout/', views.signout, name='logout'),
    path('api/register/', views.register, name='register'),
    path('api/generatecode/', views.generatecode, name='generatecode'),

    path('generatecode/', views.GenetareCodeView.as_view(), name='generatecode_page'),

    path('register/', views.RegisterView.as_view(), name='register_page'),

    path('index/', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    # path('search/', views.search, name='search'),

    path('makeposts/', views.MakePostsView.as_view(), name='makeposts_page'),
    path('api/makeposts/', views.makeposts, name='makeposts'),
    path('editpost/<int:pk>/', views.EditPostView.as_view(), name='editpost'),
    # path('editpost/<int:pk>/', views.EditPostView.as_view(), name='editpost_page'),
    # path('api/editpost/', views.editpost, name='editpost'),
    path('deletepost/<int:pk>/', views.DeletePostView.as_view(), name='deletepost'),

    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]

app_name = 'blog'
