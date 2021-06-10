{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
{% for var in env_vars %}
export {{ var.name }}="{{ var.value }}"
{% endfor %}
{{ dir_bin }}/uwsgi {{ dir_etc }}/uwsgi.ini
