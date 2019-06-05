{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
{% for var in env_vars %}
export {{ var.name }}="{{ var.value }}"
{% endfor %}
uwsgi {{ dir_etc }}/uwsgi.ini
