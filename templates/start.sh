{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
{% for var in env_vars %}
export {{ var.name }}="{{ var.value }}"
{% endfor %}
{{ dir_bin }}/gunicorn -c {{ dir_etc }}/gunicorn.conf.py
