{% if django_prefix %}
export PATH="{{ django_prefix }}/bin:$PATH"
{% endif %}
uwsgi {{ dir_etc }}/uwsgi.ini
