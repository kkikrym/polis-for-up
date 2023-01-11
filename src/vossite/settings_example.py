from pathlib import Path
import os
from distutils.util import strtobool
BASE_DIR = Path(__file__).resolve().parent.parent

#DEBUG = False
DEBUG = os.environ.get('DEBUG').lower() in ('true', 't', '1')

SECRET_KEY=os.getenv('SECRET_KEY', False)
ALLOWED_HOSTS = ['*']
ROOT_URLCONF = 'vossite.urls'


SHELL_PLUS = 'ipython'
NUMBER_GROUPING = 3

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'django_extensions',
    'channels',
    'django_summernote',
    'django_static_md5url',
    'django.contrib.humanize',


    # apps
    'top',
    'mypage',
    'chat',
    'accounts',
    'post',
    'stock',
    'community',
    'team',
    'search',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'HOST':'mysql',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'PORT': os.environ.get('MYSQL_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO,ONLY_FULL_GROUP_BY',
        },
    }
}
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
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'vossite.wsgi.application'

ASGI_APPLICATION = "vossite.asgi.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', os.environ.get('REDIS_PORT'))],
        },
    },
}

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
AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# login周り
# sitesフレームワーク用のサイトID
SITE_ID = 1

# ログイン・ログアウト時のリダイレクト先
LOGIN_REDIRECT_URL = '/mypage/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True

# 認証方式を「メルアドとパスワード」に設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ユーザ名は使用しない
ACCOUNT_USERNAME_REQUIRED = True

# ユーザ登録時に確認メールを送信するか(none=送信しない, mandatory=送信する)
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True   # ユーザ登録にメルアド必須にする


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Summernote
SUMMERNOTE_CONFIG = {
    'iframe': False,
    'summernote': {
        'width': '100%',
        'height':'500px',
        },
    'toolbar': [
            ['style', ['style']],
            ['font', ['bold',]],
            ['para', ['ul', 'ol']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['help']],
    ],

    'styleTags': [
    'p',
        { 'title': 'Blockquote', 'tag': 'blockquote', 'className': 'blockquote', 'value': 'blockquote' },
        'pre', 'h3',
	],
}

ACCOUNT_FORMS = {
    'signup': 'account.forms.CustomSignupForm',
    'login': 'account.forms.CustomLoginForm',
    'reset_password': 'account.forms.CustomResetPasswordForm',
    'reset_password_from_key': 'account.forms.CustomResetPasswordKeyForm',
    'change_password': 'account.forms.CustomChangePasswordForm',
    'add_email': 'account.forms.CustomAddEmailForm',
    'set_password': 'account.forms.CustomSetPasswordForm',
}

"""
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    }
}
"""