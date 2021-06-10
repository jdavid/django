{% if prefix %}
export PATH="{{ prefix }}/bin:$PATH"
{% endif %}
{{ dir_bin }}/uwsgi --stop {{ file_pid }}
