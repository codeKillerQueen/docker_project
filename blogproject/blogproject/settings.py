"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))


## SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'pt@51_m6vpsaegtttguk28h60xml6!$igqjkjtm(bvuo0j4w') 
SECRET_KEY = 'fvtdbs#bdshs@ghtujc6734vsv$@1edfs@sg4hhf$ghs)dd)'
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.222.129', '*']
## ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',  # 注册 blog 应用
    'comments.apps.CommentsConfig',  # 注册 comments 应用
    'pure_pagination',  # 分页
    'haystack'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blogproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogproject.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'db-mysql',  # 数据库主机，这里使用的是db别名，docker会自动解析成ip
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'Hwt123456!',  # 数据库用户密码
        'NAME': 'blogproject'  # 数据库名字
    }
}

# 设置redis缓存。这里密码为redis.conf里设置的密码
CACHES = {
     "default": {
         "BACKEND": "django_redis.cache.RedisCache",
         "LOCATION": "redis://redis:6379/1", #这里直接使用redis别名作为host ip地址
         "OPTIONS": {
             "CLIENT_CLASS": "django_redis.client.DefaultClient",
             "PASSWORD": "hwt123", # 换成你自己密码
         },
     }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/static/')

# 设置MEDIA ROOT 和 MEDIA URL
MEDIA_ROOT = os.path.join(BASE_DIR, '/media/')
MEDIA_URL = "/media/"

# django-pure-pagination 分页设置
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 4,  # 分页条当前页前后应该显示的总页数（两边均匀分布，因此要设置为偶数），
    'MARGIN_PAGES_DISPLAYED': 2,  # 分页条开头和结尾显示的页数
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,  # 当请求了不存在页，显示第一页
}

# AUTHENTICATION_BACKENDS = ('users.views.CustomBackend',)
APPEND_SLASH = False

# AUTH_USER_MODEL = 'blog.User'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

# 搜索设置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        #"ENGINE": "haystack.backends.whoosh_backend.WhooshEngine", 
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',
        # 'URL': '',
        # INDEX_NAME means?
        # 'INDEX_NAME': 'double_h',
        "PATH": os.path.join(BASE_DIR, "whoosh_index"),
    },
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 6
enable = os.environ.get("ENABLE_HAYSTACK_REALTIME_SIGNAL_PROCESSOR", "yes")
if enable in {"true", "True", "yes"}:
    HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"

HAYSTACK_CUSTOM_HIGHLIGHTER = "blog.utils.Highlighter"

HAYSTACK_CONNECTIONS['default']['URL'] = 'http://dh_elasticsearch:9200/'
