"""
This file is auto-generated by Ansible, do not modify it.
"""

from {{ django_project }}.settings import *

{% if django_database.engine == 'postgres' %}
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ django_database.name }}',
        'USER': '{{ django_database.user }}',
        'PASSWORD': '{{ django_database.password }}',
        'HOST': '',               # Set to empty string for localhost.
        'PORT': '',               # Set to empty string for default.
    }
}
{% endif %}

# Debug
DEBUG = {{ django_debug }}
{% if django_debug %}
INTERNAL_IPS = ['127.0.0.1']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AUTH_PASSWORD_VALIDATORS = []
{% endif %}

# Security
ALLOWED_HOSTS = [{% for host in django_domains %}'{{ host }}', {% endfor %}{% if django_debug %}'localhost', '127.0.0.1', '::1'{% endif %}]
SECRET_KEY = "{{ secret_key }}"

# Static
STATIC_ROOT = "{{ dir_static }}"
STATIC_URL = "{{ static_url }}"

# Media
MEDIA_ROOT = "{{ dir_media }}"
MEDIA_URL = '{{ media_url }}'
FILE_UPLOAD_PERMISSIONS = 0o644

# Sendfile
SENDFILE_BACKEND = 'sendfile.backends.{% if django_debug %}development{% else %}nginx{% endif %}'
SENDFILE_ROOT = "{{ dir_sendfile }}"
SENDFILE_URL = "{{ sendfile_url }}"

# Local settings, these should not be committed
try:
    from .settings_local import *
except ImportError:
    pass
