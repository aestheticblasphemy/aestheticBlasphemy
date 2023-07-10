"""
Django settings for aestheticBlasphemy project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

from .custom_settings import *

# Quick-start development settings - unsuitable for production

SECRET_KEY = '#nx*j2uv70r7vh-ofi8yv=1_^_&u%3jzz(#t=-fq3ga=$m_a@8'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = SITE_URLS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Own
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'mptt',
    #'treebeard',
    'blogging',
    'django_select2',
    'crispy_forms',
    'crispy_bootstrap5',
    'dashboard',
    'meta_tags',
    'django.contrib.redirects',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'taggit',
    'ckeditor',
    'ckeditor_uploader',
    'reversion',
    'pl_messages',
    'rest_framework',
    'comments',
    'django.contrib.flatpages',
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'reversion.middleware.RevisionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'reversion.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'aestheticBlasphemy.urls'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'aestheticBlasphemy.context_processors.site_processor',
                'aestheticBlasphemy.context_processors.getvars',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'pl_messages.context_processor.notifications'
            ],
        'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'aestheticBlasphemy.wsgi.application'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': DB_BASENAME,
        'HOST': '127.0.0.1',
        'USER': DB_NAME,
        'PASSWORD': DB_PASSWORD,
        'PORT': '3306',
        'TIME_ZONE': 'Asia/Kolkata',
    }
}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = TIME_ZONE_VALUE

USE_I18N = False

#USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

#STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = [
                    os.path.join(PROJECT_PATH, 'static'),
                ]

#MEDIA_ROOT = os.path.join(BASE_DIR,'media')
#MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    ]

LOGIN_REDIRECT_URL = '/'
#
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'file': {
#            'level': 'DEBUG',
#            'class': 'logging.FileHandler',
#            'filename': os.path.join(PROJECT_PATH, 'static/logs'),
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers': ['file'],
#            'level': 'DEBUG',
#            'propagate': True,
#        },
#    },
#}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
EMAIL_SUBJECT_PREFIX = '[PirateLearner]'
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'pirate_learner_mailbox'
EMAIL_HOST_PASSWORD = 'pirate@world'
SERVER_EMAIL = 'rai812@web379.webfaction.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 25
#Comments App settings
COMMENT_MODERATION_ENABLED = True

CKEDITOR_UPLOAD_PATH = 'images/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
                      ["Format", "Bold", "Italic", "Underline", "Strike", "Blockquote","Subscript", "Superscript", "SpellChecker"],
                      [ "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter',
                 'JustifyRight', 'JustifyBlock'],
                      ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink",'NumberedList', 'BulletedList', 'HorizontalRule', 'CreateDiv'],
                      ['Undo', 'Redo'], ["Source", 'RemoveFormat','Iframe'],["Maximize"],['ShowBlocks', 'Syntaxhighlight', 'Mathjax'],
                     ],
        'contentsCss': STATIC_URL+'css/bootstrap.css',

        'codemirror' : {
                        # Set this to the theme you wish to use (codemirror themes)
                        'theme': 'default',
                        # Whether or not you want to show line numbers
                        'lineNumbers': 'true',
                        # Whether or not you want to use line wrapping
                        'lineWrapping': 'true',
                        # Whether or not you want to highlight matching braces
                        'matchBrackets': 'true',
                        # Whether or not you want tags to automatically close themselves
                        'autoCloseTags': 'false',
                        # Whether or not you want Brackets to automatically close themselves
                        'autoCloseBrackets': 'false',
                        # Whether or not to enable search tools, CTRL+F (Find), CTRL+SHIFT+F (Replace), CTRL+SHIFT+R (Replace All), CTRL+G (Find Next), CTRL+SHIFT+G (Find Previous)
                        'enableSearchTools': 'true',
                        # Whether or not you wish to enable code folding (requires 'lineNumbers' to be set to 'true')
                        'enableCodeFolding': 'true',
                        # Whether or not to enable code formatting
                        'enableCodeFormatting': 'false',
                        # Whether or not to automatically format code should be done when the editor is loaded
                        'autoFormatOnStart': 'false',
                        # Whether or not to automatically format code should be done every time the source view is opened
                        'autoFormatOnModeChange': 'false',
                        # Whether or not to automatically format code which has just been uncommented
                        'autoFormatOnUncomment': 'false',
                        # Define the language specific mode 'htmlmixed' for html including (css, xml, javascript), 'application/x-httpd-php' for php mode including html, or 'text/javascript' for using java script only
                        'mode': 'htmlmixed',
                        # Whether or not to show the search Code button on the toolbar
                        'showSearchButton': 'true',
                        # Whether or not to show Trailing Spaces
                        'showTrailingSpace': 'true',
                        # Whether or not to highlight all matches of current word/selection
                        'highlightMatches': 'true',
                        # Whether or not to show the format button on the toolbar
                        'showFormatButton': 'true',
                        # Whether or not to show the comment button on the toolbar
                        'showCommentButton': 'true',
                        # Whether or not to show the uncomment button on the toolbar
                        'showUncommentButton': 'true',
                        #Whether or not to show the showAutoCompleteButton button on the toolbar
                        'showAutoCompleteButton': 'true',
                        # Whether or not to highlight the currently active line
                        'styleActiveLine': 'true'
                        },

             'disallowedContent':{
                        'p h1 h2 h3 h4 span blockquote':{
                                    #Disallow setting font-family or font-size
                                    'styles':['font*'],
                                },
                        },


            'allowedContent':{
                        '*': {

                              'attributes': ['id', 'itemprop', 'title', 'placeholder', 'type', 'data-*'],
                              'classes':['text-center', 'text-left', 'text-right', 'text-justify', 'center-text', 'text-muted',
                                         'align-center', 'pull-left', 'pull-right', 'center-block', 'media', 'image',
                                         'list-unstyled', 'list-inline',
                                         'language-*', '*',
                                        ],
                            },
                        'p': {
                                'attributes': ['id'],
                            },
                        'h1 h2 h3 h4 em i b strong caption h5 h6 u s br hr': 'true',
                        'a': {
                                'attributes': ['!href','target','name', 'id', 'name', 'rel'],
                            },
                        'img':{
                               #Do not allow image height and width styles
                               'attributes': ['!src', 'alt', 'id'],
                            },
                        'span ul ol li sup sub': 'true',
                        'div':{
                               'classes':'*',
                            },
                        'iframe':{
                                'classes':'*',
                                'attributes':'*',
                            },
                        'small abbr address footer section article dl dt dd kbd var samp form label input button textarea fieldset':'true',
                        'pre':{
                               'attributes': ['title'],
                               'classes':['*']
                            },
                        'code': 'true',

                        'blockquote':'true',
                        'table':'true',
                        'tr':'true',
                        'th':'true',
                        'td':'true',
                        },
            'justifyClasses': ['text-left', 'text-center', 'text-right', 'text-justify'],
            'extraPlugins': 'button,toolbar,codesnippet,about,stylescombo,richcombo,floatpanel,panel,button,listblock,dialog,dialogui,htmlwriter,removeformat,horizontalrule,widget,lineutils,mathjax,div,fakeobjects,iframe,image2,justify,blockquote,indent,indentlist,indentblock',
            'ignoreEmptyParagraph': 'true',
            'coreStyles_bold': {
                            'element': 'b',
                            'overrides': 'strong',
                        },
            'coreStyles_italic':{
                            'element':'i',
                            'overrides':'em',
                        },
            #'fillEmptyBlocks':'false',#Might need a callback fn
            'image2_alignClasses':['pull-left','text-center','pull-right'],
            'mathJaxClass':'math-tex',
            'mathJaxLib':STATIC_URL+'js/MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML',
            'tabSpaces':'4',
            'indentClasses': ['col-xs-offset-1', 'col-xs-offset-2', 'col-xs-offset-3', 'col-xs-offset-4'],
    },
    'author': {
        'toolbar': [
                      ["Format", "Bold", "Italic", "Underline", "Strike", "Blockquote","Subscript", "Superscript", "SpellChecker"],
                      [ "Indent", "Outdent", 'JustifyLeft', 'JustifyCenter',
                 'JustifyRight', 'JustifyBlock'],
                      ["Image", "Table", "Link", "Unlink", "Anchor", "SectionLink",'NumberedList', 'BulletedList', 'HorizontalRule', 'CreateDiv'],
                      ['Undo', 'Redo'], ["Source", 'RemoveFormat','Iframe'],["Maximize"],['ShowBlocks', 'Syntaxhighlight', 'Mathjax'],
                     ],
        'contentsCss': STATIC_URL+'css/bootstrap.css',

        'codemirror' : {
                        # Set this to the theme you wish to use (codemirror themes)
                        'theme': 'default',
                        # Whether or not you want to show line numbers
                        'lineNumbers': 'true',
                        # Whether or not you want to use line wrapping
                        'lineWrapping': 'true',
                        # Whether or not you want to highlight matching braces
                        'matchBrackets': 'true',
                        # Whether or not you want tags to automatically close themselves
                        'autoCloseTags': 'false',
                        # Whether or not you want Brackets to automatically close themselves
                        'autoCloseBrackets': 'false',
                        # Whether or not to enable search tools, CTRL+F (Find), CTRL+SHIFT+F (Replace), CTRL+SHIFT+R (Replace All), CTRL+G (Find Next), CTRL+SHIFT+G (Find Previous)
                        'enableSearchTools': 'true',
                        # Whether or not you wish to enable code folding (requires 'lineNumbers' to be set to 'true')
                        'enableCodeFolding': 'true',
                        # Whether or not to enable code formatting
                        'enableCodeFormatting': 'false',
                        # Whether or not to automatically format code should be done when the editor is loaded
                        'autoFormatOnStart': 'false',
                        # Whether or not to automatically format code should be done every time the source view is opened
                        'autoFormatOnModeChange': 'false',
                        # Whether or not to automatically format code which has just been uncommented
                        'autoFormatOnUncomment': 'false',
                        # Define the language specific mode 'htmlmixed' for html including (css, xml, javascript), 'application/x-httpd-php' for php mode including html, or 'text/javascript' for using java script only
                        'mode': 'htmlmixed',
                        # Whether or not to show the search Code button on the toolbar
                        'showSearchButton': 'true',
                        # Whether or not to show Trailing Spaces
                        'showTrailingSpace': 'true',
                        # Whether or not to highlight all matches of current word/selection
                        'highlightMatches': 'true',
                        # Whether or not to show the format button on the toolbar
                        'showFormatButton': 'true',
                        # Whether or not to show the comment button on the toolbar
                        'showCommentButton': 'true',
                        # Whether or not to show the uncomment button on the toolbar
                        'showUncommentButton': 'true',
                        #Whether or not to show the showAutoCompleteButton button on the toolbar
                        'showAutoCompleteButton': 'true',
                        # Whether or not to highlight the currently active line
                        'styleActiveLine': 'true'
                        },

             'disallowedContent':{
                        'p h1 h2 h3 h4 span blockquote':{
                                    #Disallow setting font-family or font-size
                                    'styles':['font*'],
                                },
                        },


            'allowedContent':{
                        '*': {

                              'attributes': ['id', 'itemprop', 'title', 'placeholder', 'type', 'data-*'],
                              'classes':['text-center', 'text-left', 'text-right', 'text-justify', 'center-text', 'text-muted',
                                         'align-center', 'pull-left', 'pull-right', 'center-block', 'media', 'image',
                                         'list-unstyled', 'list-inline',
                                         'language-*', '*',
                                        ],
                            },
                        'p': {
                                'attributes': ['id'],
                            },
                        'h1 h2 h3 h4 em i b strong caption h5 h6 u s br hr': 'true',
                        'a': {
                                'attributes': ['!href','target','name', 'id', 'name', 'rel'],
                            },
                        'img':{
                               #Do not allow image height and width styles
                               'attributes': ['!src', 'alt', 'id'],
                            },
                        'span ul ol li sup sub': 'true',
                        'div':{
                               'classes':'*',
                            },
                        'iframe':{
                                'classes':'*',
                                'attributes':'*',
                            },
                        'small abbr address footer section article dl dt dd kbd var samp form label input button textarea fieldset':'true',
                        'pre':{
                               'attributes': ['title'],
                               'classes':['*']
                            },
                        'code': 'true',

                        'blockquote':'true',
                        'table':'true',
                        'tr':'true',
                        'th':'true',
                        'td':'true',
                        },
            'justifyClasses': ['text-left', 'text-center', 'text-right', 'text-justify'],
            'extraPlugins': 'button,toolbar,codesnippet,about,stylescombo,richcombo,floatpanel,panel,button,listblock,dialog,dialogui,htmlwriter,removeformat,horizontalrule,widget,lineutils,mathjax,div,fakeobjects,iframe,image2,justify,blockquote,indent,indentlist,indentblock',
            'ignoreEmptyParagraph': 'true',
            'coreStyles_bold': {
                            'element': 'b',
                            'overrides': 'strong',
                        },
            'coreStyles_italic':{
                            'element':'i',
                            'overrides':'em',
                        },
            #'fillEmptyBlocks':'false',#Might netext-centerk fn
            'image2_alignClasses':['pull-left','text-center','pull-right'],
            'mathJaxClass':'math-tex',
            'mathJaxLib':STATIC_URL+'js/MathJax/MathJax.js?config=TeX-AMS-MML_HTMLorMML',
            'tabSpaces':'4',
            'indentClasses': ['col-xs-offset-1', 'col-xs-offset-2', 'col-xs-offset-3', 'col-xs-offset-4'],
    },
}
CKEDITOR_RESTRICT_BY_USER=True

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}

META_SITE_PROTOCOL = 'https'
# META_SITE_DOMAIN = 'pirateLearner.com' using META_USE_SITE SETTING
META_SITE_TYPE = 'article' # override when passed in __init__
META_SITE_NAME = 'Aesthetic Blasphemy'
#META_INCLUDE_KEYWORDS = [] # keyword will be included in every article
#META_DEFAULT_KEYWORDS = [] # default when no keyword is provided in __init__
#META_IMAGE_URL = '' # Use STATIC_URL
META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True
META_USE_SITES = True
META_PUBLISHER_FB_ID = 'https://www.facebook.com/PirateLearner' # can use PAGE URL or Publisher id ID
META_PUBLISHER_GOOGLE_ID = 'https://plus.google.com/116465481265465787624' # Google+ ID
META_FB_APP_ID = ''

#blogging app settings
BLOGGING_MAX_ENTRY_PER_PAGE = 5
BLOGGING_CSS_FRAMEWORK = 'bootstrap4'
BLOGGING_USE_REVERSION = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'verbose': {
            'format': '[%(asctime)-12s] %(message)s',
            'datefmt': '%b %d %H:%M:%S'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
        },
        #'file': {
            #'level': 'INFO',
            #'class': 'logging.FileHandler',
            #'filename': STATIC_ROOT+'/logging/log.txt',
            #'filename': '/home/craft/projects/aestheticblasphemy/aestheticBlasphemy/logs/abLog.txt',
        #},
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'PirateLearner': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
