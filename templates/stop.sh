{% if django_prefix %}
export PATH="{{ django_prefix }}/bin:$PATH"
{% endif %}
uwsgi --stop {{ file_pid }}
