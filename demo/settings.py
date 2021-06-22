import os
from decouple import config
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ALLOWED_HOSTS = ['papyrusbook-bookshoponline.fandogh.cloud']
ALLOWED_HOSTS = []


# STRIPE_PUBLIC_KEY = config('STRIPE_TEST_SECRET_KEY')
# STRIPE_SECRET_KEY = config('STRIPE_LIVE_PUBLIC_KEY')
# STRIPE_PUBLIC_KEY = config('STRRIPE_TEST_PUBLIC_KEY')
# STRIPE_SECRET_KEY = config('STRIPE_LIVE_SECRET_KEY')
LOGIN_REDIRECT_URL = "account:profile"
LOGIN_URL = "login"
LOGOUT_REDIRECT_URL = "login"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'rest_framework',


    'rest_framework.authtoken',
    'rest_auth',
    'dj_rest_auth',
    'comment',
    'star_ratings',
    'widget_tweaks',
    'bootstrap4',
    'azbankgateways',
    'core.apps.CoreConfig',
    'api.apps.ApiConfig',
    # 'account',



]

SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'papyrusbook1@gmail.com'
EMAIL_HOST_PASSWORD = 'ali13791379'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.SaveIPAdressMiddleware',
]

ROOT_URLCONF = 'demo.urls'
CRISPY_TEMPLATE_PACK = 'uni_form'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# AUTH_USER_MODEL= 'account.User'
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
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',
]


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'api.permissions.IsStaffOrReadOnly',
    ]
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ]
}


SITE_ID = 1

STAR_RATINGS_STAR_HEIGHT = 15

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
AZ_IRANIAN_BANK_GATEWAYS = {
    'GATEWAYS': {
        'IDPAY': {
            'MERCHANT_CODE': 'fba1d424-acfe-4499-a0e6-fa9ed24d353a ',
            'METHOD': 'POST',
            'X_SANDBOX': 1,
        },


    },
    'DEFAULT': 'IDPAY',
    'CURRENCY': 'IRR',
    'TRACKING_CODE_QUERY_PARAM': 'tc',
    'TRACKING_CODE_LENGTH': 16,
    'SETTING_VALUE_READER_CLASS': 'azbankgateways.readers.DefaultReader',
    'BANK_PRIORITIES': [
        'IDPAY',
        # and so on ...
    ],
}
