chdir        = '{{ django_root }}'

worker_class = 'uvicorn.workers.UvicornWorker'
workers = {{ django_server.workers|default(4) }}
threads = {{ django_server.threads|default(1) }}

wsgi_app    = 'project.asgi:application'
raw_env     =  ['DJANGO_SETTINGS_MODULE={{ settings }}']

{% if pythonpath %}
pythonpath  = '{{ pythonpath }}'
{% endif %}

# Listen
{% if django_server.port %}
bind        = ['127.0.0.1:{{ django_server.port }}']
{% else %}
bind        = ['unix:{{ file_sock }}']
{% endif %}

{% if django_with_nginx %}
daemon      = True
pidfile     = '{{ file_pid }}'

# Logging
accesslog   = '{{ dir_log }}/access.log'
errorlog    = '{{ dir_log }}/error.log'
{% endif %}
