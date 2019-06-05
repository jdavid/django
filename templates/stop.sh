{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
uwsgi --stop {{ file_pid }}
